using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x02000032 RID: 50
	[Flags]
	public enum Modifier : byte
	{
		// Token: 0x040000FD RID: 253
		Ctrl = 1,
		// Token: 0x040000FE RID: 254
		Shift = 2,
		// Token: 0x040000FF RID: 255
		Alt = 4,
		// Token: 0x04000100 RID: 256
		Win = 8,
		// Token: 0x04000101 RID: 257
		LeftCtrl = 1,
		// Token: 0x04000102 RID: 258
		LeftShift = 2,
		// Token: 0x04000103 RID: 259
		LeftAlt = 4,
		// Token: 0x04000104 RID: 260
		LeftWin = 8,
		// Token: 0x04000105 RID: 261
		RightCtrl = 16,
		// Token: 0x04000106 RID: 262
		RightShift = 32,
		// Token: 0x04000107 RID: 263
		RightAlt = 64,
		// Token: 0x04000108 RID: 264
		RightWin = 128,
		// Token: 0x04000109 RID: 265
		None = 0
	}
}
