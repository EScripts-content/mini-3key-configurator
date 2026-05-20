using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol;

namespace RSoft.MacroPad.BLL.Infrasturture.UsbDevice
{
	// Token: 0x02000011 RID: 17
	public interface IUsb
	{
		// Token: 0x1700000C RID: 12
		// (get) Token: 0x06000047 RID: 71
		bool IsConnected { get; }

		// Token: 0x1700000D RID: 13
		// (get) Token: 0x06000048 RID: 72
		// (set) Token: 0x06000049 RID: 73
		ushort VendorId { get; set; }

		// Token: 0x1700000E RID: 14
		// (get) Token: 0x0600004A RID: 74
		// (set) Token: 0x0600004B RID: 75
		ushort ProductId { get; set; }

		// Token: 0x1700000F RID: 15
		// (get) Token: 0x0600004C RID: 76
		ProtocolType ProtocolType { get; }

		// Token: 0x17000010 RID: 16
		// (get) Token: 0x0600004D RID: 77
		// (set) Token: 0x0600004E RID: 78
		byte Version { get; set; }

		// Token: 0x17000011 RID: 17
		// (get) Token: 0x0600004F RID: 79
		// (set) Token: 0x06000050 RID: 80
		[TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
		IEnumerable<ValueTuple<ushort, ushort, string, ProtocolType>> SupportedDevices
		{
			[return: TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
			get;
			[param: TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
			set;
		}

		// Token: 0x06000051 RID: 81
		bool CheckIfConnected();

		// Token: 0x06000052 RID: 82
		bool Connect();

		// Token: 0x06000053 RID: 83
		bool Write(Report report);

		// Token: 0x14000003 RID: 3
		// (add) Token: 0x06000054 RID: 84
		// (remove) Token: 0x06000055 RID: 85
		event EventHandler OnConnected;
	}
}
