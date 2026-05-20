using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using HidLibrary;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.UsbDevice
{
	// Token: 0x0200000E RID: 14
	public class HidLib
	{
		// Token: 0x17000007 RID: 7
		// (get) Token: 0x06000032 RID: 50 RVA: 0x000028DF File Offset: 0x00000ADF
		// (set) Token: 0x06000033 RID: 51 RVA: 0x000028E7 File Offset: 0x00000AE7
		public ProtocolType? ProtocolType { get; private set; }

		// Token: 0x17000008 RID: 8
		// (get) Token: 0x06000034 RID: 52 RVA: 0x000028F0 File Offset: 0x00000AF0
		// (set) Token: 0x06000035 RID: 53 RVA: 0x000028F8 File Offset: 0x00000AF8
		public ushort VendorId { get; private set; }

		// Token: 0x17000009 RID: 9
		// (get) Token: 0x06000036 RID: 54 RVA: 0x00002901 File Offset: 0x00000B01
		// (set) Token: 0x06000037 RID: 55 RVA: 0x00002909 File Offset: 0x00000B09
		public ushort ProductId { get; private set; }

		// Token: 0x1700000A RID: 10
		// (get) Token: 0x06000038 RID: 56 RVA: 0x00002912 File Offset: 0x00000B12
		public bool DeviceStatus
		{
			get
			{
				return this._deviceStatus;
			}
		}

		// Token: 0x06000039 RID: 57 RVA: 0x0000291C File Offset: 0x00000B1C
		public bool ConnectDevice([TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "ProtocolType" })] params ValueTuple<ushort, ushort, string, ProtocolType>[] supportedProducts)
		{
			foreach (ValueTuple<ushort, ushort, string, ProtocolType> valueTuple in supportedProducts)
			{
				this._hidDevice = Enumerable.FirstOrDefault<HidDevice>(HidDevices.Enumerate((int)valueTuple.Item1, new int[] { (int)valueTuple.Item2 }));
				if (this._hidDevice != null)
				{
					foreach (HidDevice hidDevice in Enumerable.ToList<HidDevice>(HidDevices.Enumerate((int)valueTuple.Item1)))
					{
						if (hidDevice.DevicePath.IndexOf(valueTuple.Item3) != -1)
						{
							this._deviceList.Add(hidDevice);
							this._hidDevice = hidDevice;
							this._hidDevice.OpenDevice();
							this.ProtocolType = new ProtocolType?(valueTuple.Item4);
							this.VendorId = valueTuple.Item1;
							this.ProductId = valueTuple.Item2;
							this._deviceStatus = true;
							return true;
						}
					}
				}
			}
			return false;
		}

		// Token: 0x0600003A RID: 58 RVA: 0x00002A30 File Offset: 0x00000C30
		public bool CheckConnection()
		{
			if (this._hidDevice.IsConnected)
			{
				return true;
			}
			this._hidDevice.CloseDevice();
			this._deviceStatus = false;
			return false;
		}

		// Token: 0x0600003B RID: 59 RVA: 0x00002A54 File Offset: 0x00000C54
		public bool WriteDevice(byte reportId, byte[] buffer)
		{
			HidReport hidReport = this._hidDevice.CreateReport();
			hidReport.ReportId = reportId;
			int num = hidReport.Data.Length;
			for (int i = 0; i < num; i++)
			{
				hidReport.Data[i] = buffer[i];
			}
			byte reportId2 = hidReport.ReportId;
			ProtocolType? protocolType = this.ProtocolType;
			ProtocolType protocolType2 = RSoft.MacroPad.BLL.Infrasturture.Model.ProtocolType.Legacy;
			IEnumerable<byte> enumerable;
			if (!((protocolType.GetValueOrDefault() == protocolType2) & (protocolType != null)))
			{
				IEnumerable<byte> data = hidReport.Data;
				enumerable = data;
			}
			else
			{
				enumerable = Enumerable.Take<byte>(hidReport.Data, 8);
			}
			HidLog.AppendMsg(reportId2, enumerable);
			return this._hidDevice.WriteReport(hidReport, 500);
		}

		// Token: 0x04000038 RID: 56
		private bool _deviceStatus;

		// Token: 0x04000039 RID: 57
		private List<HidDevice> _deviceList = new List<HidDevice>();

		// Token: 0x0400003A RID: 58
		private HidDevice _hidDevice;
	}
}
