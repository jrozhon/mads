import sys
from ctypes import c_bool, c_int

from loguru import logger
from ns import ns

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time}</green> | <level>{level}</level> | {message}",
    level="INFO",
    colorize=True,
)

first = c_int(0)


def main():
    num_switches_per_stage = 2

    # Create nodes for each stage
    logger.info("Creating nodes...")
    input_stage = ns.network.NodeContainer()
    input_stage.Create(num_switches_per_stage)

    middle_stage = ns.network.NodeContainer()
    middle_stage.Create(num_switches_per_stage)

    output_stage = ns.network.NodeContainer()
    output_stage.Create(num_switches_per_stage)
    logger.warning(output_stage)
    logger.warning(output_stage.Get(0).GetDevice(first))

    # Set up CSMA channels
    csma_helper = ns.csma.CsmaHelper()

    # Connect stages
    net_devices = []
    for i in range(num_switches_per_stage):
        for j in range(num_switches_per_stage):
            temp_container = ns.network.NodeContainer()
            temp_container.Add(input_stage.Get(i))
            temp_container.Add(middle_stage.Get(j))
            net_devices.append(csma_helper.Install(temp_container))

            temp_container = ns.network.NodeContainer()
            temp_container.Add(middle_stage.Get(i))
            temp_container.Add(output_stage.Get(j))
            net_devices.append(csma_helper.Install(temp_container))

    # Add Internet stack
    internet = ns.internet.InternetStackHelper()
    internet.InstallAll()

    # Assign IP addresses
    addresses = []
    address = ns.internet.Ipv4AddressHelper()
    subnet = 1
    for devices in net_devices:
        base_ip = "10." + str(subnet) + ".1.0"
        address.SetBase(
            ns.network.Ipv4Address(base_ip), ns.network.Ipv4Mask("255.255.255.0")
        )
        addresses.append(address.Assign(devices))
        subnet += 1

    print(addresses)

    # Set up traffic
    sourceApps = ns.network.ApplicationContainer()
    destApps = ns.network.ApplicationContainer()

    for i in range(num_switches_per_stage):
        onoff_helper = ns.applications.OnOffHelper(
            "ns3::UdpSocketFactory", ns.network.Address()
        )
        onoff_helper.SetAttribute(
            "OnTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=1]")
        )
        onoff_helper.SetAttribute(
            "OffTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=0]")
        )

        # remote_addr = ns.network.InetSocketAddress(output_stage.Get(i).GetObject(ns.internet.Ipv4.GetTypeId()).GetAddress(1,0).GetLocal(), 9)
        # ipv4_obj = ns.internet.Ipv4AddressHelper.GetIpv4(output_stage.Get(i))
        # ipv4_obj = output_stage.Get(i).GetObject(ns.internet.Ipv4.GetTypeId())
        # ipv4_obj = output_stage.Get(i).GetObject(ns.internet.Ipv4.GetTypeId()).GetObject(ns.internet.Ipv4)
        print(output_stage.Get(i))
        ipv4_obj = output_stage.Get(i).GetObject(ns.internet.Ipv4.GetTypeId())
        remote_addr = ns.network.InetSocketAddress(
            ipv4_obj.GetAddress(1, 0).GetLocal(), 9
        )

        onoff_helper.SetAttribute("Remote", ns.network.AddressValue(remote_addr))

        sourceApps.Add(onoff_helper.Install(input_stage.Get(i)))

        # Set up packet sinks at the receivers to capture packets
        packet_sink_helper = ns.applications.PacketSinkHelper(
            "ns3::UdpSocketFactory", ns.network.Address(remote_addr)
        )
        destApps.Add(packet_sink_helper.Install(output_stage.Get(i)))

    sourceApps.Start(ns.core.Seconds(1.0))
    sourceApps.Stop(ns.core.Seconds(10.0))
    destApps.Start(ns.core.Seconds(1.0))
    destApps.Stop(ns.core.Seconds(10.0))

    # Setup FlowMonitor
    flow_monitor_helper = ns.flow_monitor.FlowMonitorHelper()
    monitor = flow_monitor_helper.InstallAll()

    # Set up NetAnim
    animator = ns.netanim.AnimationInterface("clos-animation.xml")

    ns.core.Simulator.Run()

    # Analyze and print results
    monitor.CheckForLostPackets()
    classifier = flow_monitor_helper.GetClassifier()
    stats = monitor.GetFlowStats()

    for i, stat in enumerate(stats):
        if not stat.rxPackets:
            print(
                "Flow",
                i,
                "(from node",
                classifier.GetFlow(i).sourceAddress,
                "to",
                classifier.GetFlow(i).destinationAddress,
                ") is blocked!",
            )
        else:
            print(
                "Flow",
                i,
                "(from node",
                classifier.GetFlow(i).sourceAddress,
                "to",
                classifier.GetFlow(i).destinationAddress,
                ") has throughput of",
                stat.rxBytes * 8.0 / 9.0 / 1e3,
                "kbps",
            )

    ns.core.Simulator.Destroy()


if __name__ == "__main__":
    main()
