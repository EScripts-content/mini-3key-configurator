using System;

namespace HID
{
	// Token: 0x02000007 RID: 7
	public struct SP_DEVICE_INTERFACE_DATA
	{
		// Token: 0x0400002A RID: 42
		public int cbSize;

		// Token: 0x0400002B RID: 43
		public Guid interfaceClassGuid;

		// Token: 0x0400002C RID: 44
		public int flags;

		// Token: 0x0400002D RID: 45
		public int reserved;
	}
}
