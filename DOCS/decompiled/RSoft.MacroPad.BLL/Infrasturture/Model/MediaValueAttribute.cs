using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x02000031 RID: 49
	[AttributeUsage(256, AllowMultiple = true)]
	public class MediaValueAttribute : Attribute
	{
		// Token: 0x1700002A RID: 42
		// (get) Token: 0x060000C6 RID: 198 RVA: 0x00003FE2 File Offset: 0x000021E2
		public byte B1 { get; }

		// Token: 0x1700002B RID: 43
		// (get) Token: 0x060000C7 RID: 199 RVA: 0x00003FEA File Offset: 0x000021EA
		public byte B2 { get; }

		// Token: 0x1700002C RID: 44
		// (get) Token: 0x060000C8 RID: 200 RVA: 0x00003FF2 File Offset: 0x000021F2
		public byte Version { get; }

		// Token: 0x060000C9 RID: 201 RVA: 0x00003FFA File Offset: 0x000021FA
		public MediaValueAttribute(byte version, byte b1, byte b2)
		{
			this.Version = version;
			this.B1 = b1;
			this.B2 = b2;
		}
	}
}
