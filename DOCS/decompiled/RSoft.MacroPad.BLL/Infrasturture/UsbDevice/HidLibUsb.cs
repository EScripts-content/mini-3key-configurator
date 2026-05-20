using System;
using System.Linq;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol;

namespace RSoft.MacroPad.BLL.Infrasturture.UsbDevice
{
	// Token: 0x0200000F RID: 15
	public class HidLibUsb : UsbBase
	{
		// Token: 0x1700000B RID: 11
		// (get) Token: 0x0600003D RID: 61 RVA: 0x00002AFA File Offset: 0x00000CFA
		// (set) Token: 0x0600003E RID: 62 RVA: 0x00002B02 File Offset: 0x00000D02
		public string PathFragment { get; set; }

		// Token: 0x0600003F RID: 63 RVA: 0x00002B0B File Offset: 0x00000D0B
		public override bool Write(Report report)
		{
			return this._hidLib.WriteDevice(report.ReportId, report.Data);
		}

		// Token: 0x06000040 RID: 64 RVA: 0x00002B24 File Offset: 0x00000D24
		protected override bool CheckIfConnectedInternal()
		{
			return base.IsConnected = this._hidLib.DeviceStatus && this._hidLib.CheckConnection();
		}

		// Token: 0x06000041 RID: 65 RVA: 0x00002B58 File Offset: 0x00000D58
		protected override bool ConnectInternal()
		{
			if (this._hidLib.ConnectDevice(Enumerable.ToArray<ValueTuple<ushort, ushort, string, ProtocolType>>(base.SupportedDevices)))
			{
				base.ProductId = this._hidLib.ProductId;
				base.VendorId = this._hidLib.VendorId;
				base.ProtocolType = this._hidLib.ProtocolType.Value;
				base.Connected();
				return base.IsConnected = true;
			}
			return base.IsConnected = false;
		}

		// Token: 0x0400003E RID: 62
		private HidLib _hidLib = new HidLib();
	}
}
