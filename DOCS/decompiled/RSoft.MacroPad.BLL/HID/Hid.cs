using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using Microsoft.Win32.SafeHandles;

namespace HID
{
	// Token: 0x02000002 RID: 2
	public class Hid
	{
		// Token: 0x17000001 RID: 1
		// (get) Token: 0x06000001 RID: 1 RVA: 0x00002050 File Offset: 0x00000250
		public int OutputReportLength
		{
			get
			{
				return this.outputReportLength;
			}
		}

		// Token: 0x17000002 RID: 2
		// (get) Token: 0x06000002 RID: 2 RVA: 0x00002058 File Offset: 0x00000258
		public int InputReportLength
		{
			get
			{
				return this.inputReportLength;
			}
		}

		// Token: 0x06000003 RID: 3 RVA: 0x00002060 File Offset: 0x00000260
		public static Hid.HID_RETURN GetDeviceSerialList(ushort vID, ushort pID, ref List<string> serialList)
		{
			serialList.Clear();
			List<string> list = new List<string>();
			Hid.GetHidDeviceList(ref list);
			if (list.Count == 0)
			{
				return Hid.HID_RETURN.NO_DEVICE_CONECTED;
			}
			for (int i = 0; i < list.Count; i++)
			{
				IntPtr intPtr = Hid.CreateFile(list[i], 3221225472U, 0U, 0U, 3U, 1073741824U, 0U);
				if (intPtr != Hid.INVALID_HANDLE_VALUE)
				{
					IntPtr intPtr2 = Marshal.AllocHGlobal(512);
					HIDD_ATTRIBUTES hidd_ATTRIBUTES;
					Hid.HidD_GetAttributes(intPtr, out hidd_ATTRIBUTES);
					Hid.HidD_GetSerialNumberString(intPtr, intPtr2, 512);
					string text = Marshal.PtrToStringAuto(intPtr2);
					Marshal.FreeHGlobal(intPtr2);
					if (hidd_ATTRIBUTES.VendorID == vID && hidd_ATTRIBUTES.ProductID == pID)
					{
						serialList.Add(text);
					}
					Hid.CloseHandle(intPtr);
				}
			}
			return Hid.HID_RETURN.SUCCESS;
		}

		// Token: 0x06000004 RID: 4 RVA: 0x0000211C File Offset: 0x0000031C
		public IntPtr OpenDevice(ushort vID, ushort pID)
		{
			if (this.deviceOpened)
			{
				return Hid.INVALID_HANDLE_VALUE;
			}
			List<string> list = new List<string>();
			Hid.GetHidDeviceList(ref list);
			if (list.Count == 0)
			{
				return Hid.INVALID_HANDLE_VALUE;
			}
			for (int i = 0; i < list.Count; i++)
			{
				IntPtr intPtr = Hid.CreateFile(list[i], 3221225472U, 0U, 0U, 3U, 1073741824U, 0U);
				if (intPtr != Hid.INVALID_HANDLE_VALUE)
				{
					IntPtr intPtr2 = Marshal.AllocHGlobal(512);
					HIDD_ATTRIBUTES hidd_ATTRIBUTES;
					if (!Hid.HidD_GetAttributes(intPtr, out hidd_ATTRIBUTES))
					{
						Hid.CloseHandle(intPtr);
						return Hid.INVALID_HANDLE_VALUE;
					}
					Hid.HidD_GetSerialNumberString(intPtr, intPtr2, 512);
					Marshal.PtrToStringAuto(intPtr2);
					Marshal.FreeHGlobal(intPtr2);
					if (hidd_ATTRIBUTES.VendorID == vID && hidd_ATTRIBUTES.ProductID == pID)
					{
						IntPtr intPtr3;
						Hid.HidD_GetPreparsedData(intPtr, out intPtr3);
						HIDP_CAPS hidp_CAPS;
						Hid.HidP_GetCaps(intPtr3, out hidp_CAPS);
						Hid.HidD_FreePreparsedData(intPtr3);
						this.outputReportLength = (int)hidp_CAPS.OutputReportByteLength;
						this.inputReportLength = (int)hidp_CAPS.InputReportByteLength;
						this.hidDevice = new FileStream(new SafeFileHandle(intPtr, false), 3, this.inputReportLength, true);
						this.deviceOpened = true;
						this.BeginAsyncRead();
						return intPtr;
					}
				}
				Hid.CloseHandle(intPtr);
			}
			return Hid.INVALID_HANDLE_VALUE;
		}

		// Token: 0x17000003 RID: 3
		// (get) Token: 0x06000005 RID: 5 RVA: 0x0000224E File Offset: 0x0000044E
		public bool Opened
		{
			get
			{
				return this.deviceOpened;
			}
		}

		// Token: 0x06000006 RID: 6 RVA: 0x00002256 File Offset: 0x00000456
		public void CloseDevice(IntPtr device)
		{
			if (!this.deviceOpened)
			{
				return;
			}
			this.deviceOpened = false;
			this.hidDevice.Close();
			Hid.CloseHandle(device);
		}

		// Token: 0x06000007 RID: 7 RVA: 0x0000227C File Offset: 0x0000047C
		private void BeginAsyncRead()
		{
			byte[] array = new byte[this.InputReportLength];
			IntPtr handle = this.hidDevice.Handle;
			this.readResult = this.hidDevice.BeginRead(array, 0, this.InputReportLength, new AsyncCallback(this.ReadCompleted), array);
		}

		// Token: 0x06000008 RID: 8 RVA: 0x000022C8 File Offset: 0x000004C8
		private void ReadCompleted(IAsyncResult iResult)
		{
			byte[] array = (byte[])iResult.AsyncState;
			try
			{
				if (this.deviceOpened)
				{
					this.hidDevice.EndRead(iResult);
					byte[] array2 = new byte[array.Length - 1];
					for (int i = 1; i < array.Length; i++)
					{
						array2[i - 1] = array[i];
					}
					this.OnDataReceived(new report(array[0], array2));
					this.BeginAsyncRead();
				}
			}
			catch (IOException)
			{
				this.OnDeviceRemoved(new EventArgs());
			}
		}

		// Token: 0x14000001 RID: 1
		// (add) Token: 0x06000009 RID: 9 RVA: 0x00002350 File Offset: 0x00000550
		// (remove) Token: 0x0600000A RID: 10 RVA: 0x00002388 File Offset: 0x00000588
		public event EventHandler<report> DataReceived;

		// Token: 0x0600000B RID: 11 RVA: 0x000023BD File Offset: 0x000005BD
		protected virtual void OnDataReceived(report e)
		{
			if (this.DataReceived == null)
			{
				return;
			}
			this.DataReceived.Invoke(this, e);
		}

		// Token: 0x14000002 RID: 2
		// (add) Token: 0x0600000C RID: 12 RVA: 0x000023D8 File Offset: 0x000005D8
		// (remove) Token: 0x0600000D RID: 13 RVA: 0x00002410 File Offset: 0x00000610
		public event EventHandler DeviceRemoved;

		// Token: 0x0600000E RID: 14 RVA: 0x00002445 File Offset: 0x00000645
		protected virtual void OnDeviceRemoved(EventArgs e)
		{
			this.deviceOpened = false;
			if (this.DeviceRemoved == null)
			{
				return;
			}
			this.DeviceRemoved.Invoke(this, e);
		}

		// Token: 0x0600000F RID: 15 RVA: 0x00002464 File Offset: 0x00000664
		public Hid.HID_RETURN Write(report r)
		{
			if (this.deviceOpened)
			{
				try
				{
					byte[] array = new byte[this.outputReportLength];
					array[0] = r.reportID;
					int num = ((r.reportBuff.Length >= this.outputReportLength - 1) ? (this.outputReportLength - 1) : r.reportBuff.Length);
					for (int i = 1; i <= num; i++)
					{
						array[i] = r.reportBuff[i - 1];
					}
					this.hidDevice.Write(array, 0, 65);
					return Hid.HID_RETURN.SUCCESS;
				}
				catch
				{
				}
				return Hid.HID_RETURN.WRITE_FAILD;
			}
			return Hid.HID_RETURN.WRITE_FAILD;
		}

		// Token: 0x06000010 RID: 16 RVA: 0x000024F8 File Offset: 0x000006F8
		public static void GetHidDeviceList(ref List<string> deviceList)
		{
			Guid empty = Guid.Empty;
			deviceList.Clear();
			Hid.HidD_GetHidGuid(ref empty);
			IntPtr intPtr = Hid.SetupDiGetClassDevs(ref empty, 0U, IntPtr.Zero, (DIGCF)18);
			if (intPtr != IntPtr.Zero)
			{
				SP_DEVICE_INTERFACE_DATA sp_DEVICE_INTERFACE_DATA = default(SP_DEVICE_INTERFACE_DATA);
				sp_DEVICE_INTERFACE_DATA.cbSize = Marshal.SizeOf(sp_DEVICE_INTERFACE_DATA);
				for (uint num = 0U; num < 64U; num += 1U)
				{
					if (Hid.SetupDiEnumDeviceInterfaces(intPtr, IntPtr.Zero, ref empty, num, ref sp_DEVICE_INTERFACE_DATA))
					{
						int num2 = 0;
						Hid.SetupDiGetDeviceInterfaceDetail(intPtr, ref sp_DEVICE_INTERFACE_DATA, IntPtr.Zero, num2, ref num2, null);
						IntPtr intPtr2 = Marshal.AllocHGlobal(num2);
						Marshal.StructureToPtr(new SP_DEVICE_INTERFACE_DETAIL_DATA
						{
							cbSize = Marshal.SizeOf(typeof(SP_DEVICE_INTERFACE_DETAIL_DATA))
						}, intPtr2, false);
						if (Hid.SetupDiGetDeviceInterfaceDetail(intPtr, ref sp_DEVICE_INTERFACE_DATA, intPtr2, num2, ref num2, null))
						{
							deviceList.Add(Marshal.PtrToStringAuto((IntPtr)((int)intPtr2 + 4)));
						}
						Marshal.FreeHGlobal(intPtr2);
					}
				}
			}
			Hid.SetupDiDestroyDeviceInfoList(intPtr);
		}

		// Token: 0x06000011 RID: 17
		[DllImport("hid.dll")]
		private static extern void HidD_GetHidGuid(ref Guid HidGuid);

		// Token: 0x06000012 RID: 18
		[DllImport("setupapi.dll", SetLastError = true)]
		private static extern IntPtr SetupDiGetClassDevs(ref Guid ClassGuid, uint Enumerator, IntPtr HwndParent, DIGCF Flags);

		// Token: 0x06000013 RID: 19
		[DllImport("setupapi.dll", CharSet = 4, SetLastError = true)]
		private static extern bool SetupDiDestroyDeviceInfoList(IntPtr deviceInfoSet);

		// Token: 0x06000014 RID: 20
		[DllImport("setupapi.dll", CharSet = 4, SetLastError = true)]
		private static extern bool SetupDiEnumDeviceInterfaces(IntPtr deviceInfoSet, IntPtr deviceInfoData, ref Guid interfaceClassGuid, uint memberIndex, ref SP_DEVICE_INTERFACE_DATA deviceInterfaceData);

		// Token: 0x06000015 RID: 21
		[DllImport("setupapi.dll", CharSet = 4, SetLastError = true)]
		private static extern bool SetupDiGetDeviceInterfaceDetail(IntPtr deviceInfoSet, ref SP_DEVICE_INTERFACE_DATA deviceInterfaceData, IntPtr deviceInterfaceDetailData, int deviceInterfaceDetailDataSize, ref int requiredSize, SP_DEVINFO_DATA deviceInfoData);

		// Token: 0x06000016 RID: 22
		[DllImport("hid.dll")]
		private static extern bool HidD_GetAttributes(IntPtr hidDeviceObject, out HIDD_ATTRIBUTES attributes);

		// Token: 0x06000017 RID: 23
		[DllImport("hid.dll")]
		private static extern bool HidD_GetSerialNumberString(IntPtr hidDeviceObject, IntPtr buffer, int bufferLength);

		// Token: 0x06000018 RID: 24
		[DllImport("hid.dll")]
		private static extern bool HidD_GetPreparsedData(IntPtr hidDeviceObject, out IntPtr PreparsedData);

		// Token: 0x06000019 RID: 25
		[DllImport("hid.dll")]
		private static extern bool HidD_FreePreparsedData(IntPtr PreparsedData);

		// Token: 0x0600001A RID: 26
		[DllImport("hid.dll")]
		private static extern uint HidP_GetCaps(IntPtr PreparsedData, out HIDP_CAPS Capabilities);

		// Token: 0x0600001B RID: 27
		[DllImport("kernel32.dll", SetLastError = true)]
		private static extern IntPtr CreateFile(string fileName, uint desiredAccess, uint shareMode, uint securityAttributes, uint creationDisposition, uint flagsAndAttributes, uint templateFile);

		// Token: 0x0600001C RID: 28
		[DllImport("kernel32.dll")]
		private static extern int CloseHandle(IntPtr hObject);

		// Token: 0x0600001D RID: 29
		[DllImport("Kernel32.dll", SetLastError = true)]
		private static extern bool ReadFile(IntPtr file, byte[] buffer, uint numberOfBytesToRead, out uint numberOfBytesRead, IntPtr lpOverlapped);

		// Token: 0x0600001E RID: 30
		[DllImport("Kernel32.dll", SetLastError = true)]
		private static extern bool WriteFile(IntPtr file, byte[] buffer, uint numberOfBytesToWrite, out uint numberOfBytesWritten, IntPtr lpOverlapped);

		// Token: 0x0600001F RID: 31
		[DllImport("User32.dll", SetLastError = true)]
		private static extern IntPtr RegisterDeviceNotification(IntPtr recipient, IntPtr notificationFilter, int flags);

		// Token: 0x06000020 RID: 32 RVA: 0x00002600 File Offset: 0x00000800
		public static IntPtr RegisterHIDNotification(IntPtr recipient)
		{
			IntPtr intPtr = Marshal.AllocHGlobal(Marshal.SizeOf(typeof(Hid.DevBroadcastDeviceInterfaceBuffer)));
			Marshal.StructureToPtr(new Hid.DevBroadcastDeviceInterfaceBuffer(5), intPtr, false);
			return Hid.RegisterDeviceNotification(recipient, intPtr, 0);
		}

		// Token: 0x06000021 RID: 33
		[DllImport("user32.dll", SetLastError = true)]
		private static extern bool UnregisterDeviceNotification(IntPtr handle);

		// Token: 0x06000022 RID: 34 RVA: 0x0000263C File Offset: 0x0000083C
		public static bool UnRegisterHIDNotification(IntPtr hDEVNotify)
		{
			return Hid.UnregisterDeviceNotification(hDEVNotify);
		}

		// Token: 0x04000001 RID: 1
		public const uint GENERIC_READ = 2147483648U;

		// Token: 0x04000002 RID: 2
		public const uint GENERIC_WRITE = 1073741824U;

		// Token: 0x04000003 RID: 3
		public const uint FILE_SHARE_READ = 1U;

		// Token: 0x04000004 RID: 4
		public const uint FILE_SHARE_WRITE = 2U;

		// Token: 0x04000005 RID: 5
		public const int OPEN_EXISTING = 3;

		// Token: 0x04000006 RID: 6
		private static IntPtr INVALID_HANDLE_VALUE = new IntPtr(-1);

		// Token: 0x04000007 RID: 7
		private const int MAX_USB_DEVICES = 64;

		// Token: 0x04000008 RID: 8
		private bool deviceOpened;

		// Token: 0x04000009 RID: 9
		private FileStream hidDevice;

		// Token: 0x0400000A RID: 10
		private IAsyncResult readResult;

		// Token: 0x0400000B RID: 11
		private int outputReportLength;

		// Token: 0x0400000C RID: 12
		private int inputReportLength;

		// Token: 0x0200003A RID: 58
		public enum HID_RETURN
		{
			// Token: 0x040001DC RID: 476
			SUCCESS,
			// Token: 0x040001DD RID: 477
			NO_DEVICE_CONECTED,
			// Token: 0x040001DE RID: 478
			DEVICE_NOT_FIND,
			// Token: 0x040001DF RID: 479
			DEVICE_OPENED,
			// Token: 0x040001E0 RID: 480
			WRITE_FAILD,
			// Token: 0x040001E1 RID: 481
			READ_FAILD
		}

		// Token: 0x0200003B RID: 59
		[StructLayout(2)]
		private struct DevBroadcastDeviceInterfaceBuffer
		{
			// Token: 0x060000D4 RID: 212 RVA: 0x00004254 File Offset: 0x00002454
			public DevBroadcastDeviceInterfaceBuffer(int deviceType)
			{
				this.dbch_size = Marshal.SizeOf(typeof(Hid.DevBroadcastDeviceInterfaceBuffer));
				this.dbch_devicetype = deviceType;
				this.dbch_reserved = 0;
			}

			// Token: 0x040001E2 RID: 482
			[FieldOffset(0)]
			public int dbch_size;

			// Token: 0x040001E3 RID: 483
			[FieldOffset(4)]
			public int dbch_devicetype;

			// Token: 0x040001E4 RID: 484
			[FieldOffset(8)]
			public int dbch_reserved;
		}
	}
}
