using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x02000033 RID: 51
	public enum MouseButton
	{
		// Token: 0x0400010B RID: 267
		[MouseValues(1, 0)]
		Left,
		// Token: 0x0400010C RID: 268
		[MouseValues(4, 0)]
		Middle,
		// Token: 0x0400010D RID: 269
		[MouseValues(2, 0)]
		Right,
		// Token: 0x0400010E RID: 270
		[MouseValues(0, 1)]
		ScrollUp,
		// Token: 0x0400010F RID: 271
		[MouseValues(0, 255)]
		ScrollDown
	}
}
