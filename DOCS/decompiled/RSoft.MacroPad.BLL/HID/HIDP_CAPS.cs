using System;
using System.Runtime.InteropServices;

namespace HID
{
	// Token: 0x02000005 RID: 5
	public struct HIDP_CAPS
	{
		// Token: 0x04000019 RID: 25
		public ushort Usage;

		// Token: 0x0400001A RID: 26
		public ushort UsagePage;

		// Token: 0x0400001B RID: 27
		public ushort InputReportByteLength;

		// Token: 0x0400001C RID: 28
		public ushort OutputReportByteLength;

		// Token: 0x0400001D RID: 29
		[MarshalAs(30, SizeConst = 17)]
		public ushort[] Reserved;

		// Token: 0x0400001E RID: 30
		public ushort NumberLinkCollectionNodes;

		// Token: 0x0400001F RID: 31
		public ushort NumberInputButtonCaps;

		// Token: 0x04000020 RID: 32
		public ushort NumberInputValueCaps;

		// Token: 0x04000021 RID: 33
		public ushort NumberInputDataIndices;

		// Token: 0x04000022 RID: 34
		public ushort NumberOutputButtonCaps;

		// Token: 0x04000023 RID: 35
		public ushort NumberOutputValueCaps;

		// Token: 0x04000024 RID: 36
		public ushort NumberOutputDataIndices;

		// Token: 0x04000025 RID: 37
		public ushort NumberFeatureButtonCaps;

		// Token: 0x04000026 RID: 38
		public ushort NumberFeatureValueCaps;

		// Token: 0x04000027 RID: 39
		public ushort NumberFeatureDataIndices;
	}
}
