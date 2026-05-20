using System;
using System.Runtime.InteropServices;

namespace HID
{
	// Token: 0x02000009 RID: 9
	[StructLayout(0)]
	public class SP_DEVINFO_DATA
	{
		// Token: 0x04000030 RID: 48
		public int cbSize = Marshal.SizeOf(typeof(SP_DEVINFO_DATA));

		// Token: 0x04000031 RID: 49
		public Guid classGuid = Guid.Empty;

		// Token: 0x04000032 RID: 50
		public int devInst;

		// Token: 0x04000033 RID: 51
		public int reserved;
	}
}
