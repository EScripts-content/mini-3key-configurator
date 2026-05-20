using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.UsbDevice
{
	// Token: 0x0200000D RID: 13
	public static class DeviceSample
	{
		// Token: 0x17000005 RID: 5
		// (get) Token: 0x0600002E RID: 46 RVA: 0x00002806 File Offset: 0x00000A06
		// (set) Token: 0x0600002F RID: 47 RVA: 0x0000280D File Offset: 0x00000A0D
		public static int VendorId { get; set; } = 4489;

		// Token: 0x17000006 RID: 6
		// (get) Token: 0x06000030 RID: 48 RVA: 0x00002818 File Offset: 0x00000A18
		[TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
		public static IEnumerable<ValueTuple<ushort, ushort, string, ProtocolType>> Devices
		{
			[return: TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
			get
			{
				return new ValueTuple<ushort, ushort, string, ProtocolType>[]
				{
					new ValueTuple<ushort, ushort, string, ProtocolType>(4489, 34960, "mi_01", ProtocolType.Legacy),
					new ValueTuple<ushort, ushort, string, ProtocolType>(4489, 34864, "mi_00", ProtocolType.Extended),
					new ValueTuple<ushort, ushort, string, ProtocolType>(4489, 34865, "mi_00", ProtocolType.Extended),
					new ValueTuple<ushort, ushort, string, ProtocolType>(4489, 34866, "mi_00", ProtocolType.Extended),
					new ValueTuple<ushort, ushort, string, ProtocolType>(4489, 34967, "mi_00", ProtocolType.Extended),
					new ValueTuple<ushort, ushort, string, ProtocolType>(4489, 34932, "mi_00", ProtocolType.Extended)
				};
			}
		}
	}
}
