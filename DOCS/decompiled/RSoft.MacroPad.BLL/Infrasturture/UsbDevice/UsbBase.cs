using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol;

namespace RSoft.MacroPad.BLL.Infrasturture.UsbDevice
{
	// Token: 0x02000012 RID: 18
	public abstract class UsbBase : IUsb
	{
		// Token: 0x17000012 RID: 18
		// (get) Token: 0x06000056 RID: 86 RVA: 0x00002CF3 File Offset: 0x00000EF3
		// (set) Token: 0x06000057 RID: 87 RVA: 0x00002CFB File Offset: 0x00000EFB
		public ushort VendorId { get; set; }

		// Token: 0x17000013 RID: 19
		// (get) Token: 0x06000058 RID: 88 RVA: 0x00002D04 File Offset: 0x00000F04
		// (set) Token: 0x06000059 RID: 89 RVA: 0x00002D0C File Offset: 0x00000F0C
		public ushort ProductId { get; set; }

		// Token: 0x17000014 RID: 20
		// (get) Token: 0x0600005A RID: 90 RVA: 0x00002D15 File Offset: 0x00000F15
		// (set) Token: 0x0600005B RID: 91 RVA: 0x00002D1D File Offset: 0x00000F1D
		public ProtocolType ProtocolType { get; protected set; }

		// Token: 0x17000015 RID: 21
		// (get) Token: 0x0600005C RID: 92 RVA: 0x00002D26 File Offset: 0x00000F26
		// (set) Token: 0x0600005D RID: 93 RVA: 0x00002D2E File Offset: 0x00000F2E
		public byte Version { get; set; }

		// Token: 0x14000004 RID: 4
		// (add) Token: 0x0600005E RID: 94 RVA: 0x00002D38 File Offset: 0x00000F38
		// (remove) Token: 0x0600005F RID: 95 RVA: 0x00002D70 File Offset: 0x00000F70
		public event EventHandler OnConnected;

		// Token: 0x06000060 RID: 96 RVA: 0x00002DA5 File Offset: 0x00000FA5
		public bool CheckIfConnected()
		{
			return this.CheckIfConnectedInternal();
		}

		// Token: 0x17000016 RID: 22
		// (get) Token: 0x06000061 RID: 97 RVA: 0x00002DAD File Offset: 0x00000FAD
		// (set) Token: 0x06000062 RID: 98 RVA: 0x00002DB5 File Offset: 0x00000FB5
		[TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
		public IEnumerable<ValueTuple<ushort, ushort, string, ProtocolType>> SupportedDevices
		{
			[return: TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
			get;
			[param: TupleElementNames(new string[] { "VendorId", "ProductId", "PathFragment", "protocolType" })]
			set;
		} = DeviceSample.Devices;

		// Token: 0x17000017 RID: 23
		// (get) Token: 0x06000063 RID: 99 RVA: 0x00002DBE File Offset: 0x00000FBE
		// (set) Token: 0x06000064 RID: 100 RVA: 0x00002DC6 File Offset: 0x00000FC6
		public bool IsConnected { get; protected set; }

		// Token: 0x06000065 RID: 101
		protected abstract bool CheckIfConnectedInternal();

		// Token: 0x06000066 RID: 102 RVA: 0x00002DCF File Offset: 0x00000FCF
		public bool Connect()
		{
			return this.CheckIfConnectedInternal() || this.ConnectInternal();
		}

		// Token: 0x06000067 RID: 103
		protected abstract bool ConnectInternal();

		// Token: 0x06000068 RID: 104 RVA: 0x00002DE4 File Offset: 0x00000FE4
		protected virtual byte KeyBoardVersionCheck()
		{
			if (this.Write(VersionCheckReport.Create(0)))
			{
				return this.Version = 0;
			}
			if (this.Write(VersionCheckReport.Create(2)))
			{
				return this.Version = 2;
			}
			return this.Version = 3;
		}

		// Token: 0x06000069 RID: 105 RVA: 0x00002E2D File Offset: 0x0000102D
		protected void Connected()
		{
			this.KeyBoardVersionCheck();
			EventHandler onConnected = this.OnConnected;
			if (onConnected == null)
			{
				return;
			}
			onConnected.Invoke(this, EventArgs.Empty);
		}

		// Token: 0x0600006A RID: 106
		public abstract bool Write(Report report);
	}
}
