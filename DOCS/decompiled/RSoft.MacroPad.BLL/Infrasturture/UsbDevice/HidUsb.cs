using System;
using HID;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol;

namespace RSoft.MacroPad.BLL.Infrasturture.UsbDevice
{
	// Token: 0x02000010 RID: 16
	public class HidUsb : UsbBase
	{
		// Token: 0x06000043 RID: 67 RVA: 0x00002BE6 File Offset: 0x00000DE6
		public override bool Write(Report report)
		{
			return this._hid.Write(new report(report.ReportId, report.Data)) == Hid.HID_RETURN.SUCCESS;
		}

		// Token: 0x06000044 RID: 68 RVA: 0x00002C08 File Offset: 0x00000E08
		protected override bool CheckIfConnectedInternal()
		{
			return base.IsConnected = this._hid.Opened;
		}

		// Token: 0x06000045 RID: 69 RVA: 0x00002C2C File Offset: 0x00000E2C
		protected override bool ConnectInternal()
		{
			foreach (ValueTuple<ushort, ushort, string, ProtocolType> valueTuple in base.SupportedDevices)
			{
				if ((int)(this._hidPtr = this._hid.OpenDevice(valueTuple.Item1, valueTuple.Item2)) != -1)
				{
					base.VendorId = valueTuple.Item1;
					base.ProductId = valueTuple.Item2;
					base.ProtocolType = valueTuple.Item4;
					base.Connected();
					return base.IsConnected = true;
				}
			}
			return base.IsConnected = false;
		}

		// Token: 0x04000040 RID: 64
		private Hid _hid = new Hid();

		// Token: 0x04000041 RID: 65
		private IntPtr _hidPtr;
	}
}
