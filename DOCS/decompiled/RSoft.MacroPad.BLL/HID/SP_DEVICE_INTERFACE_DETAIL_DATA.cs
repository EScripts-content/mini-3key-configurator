using System;
using System.Runtime.InteropServices;

namespace HID
{
	// Token: 0x02000008 RID: 8
	[StructLayout(0, Pack = 2)]
	internal struct SP_DEVICE_INTERFACE_DETAIL_DATA
	{
		// Token: 0x0400002E RID: 46
		internal int cbSize;

		// Token: 0x0400002F RID: 47
		internal short devicePath;
	}
}
