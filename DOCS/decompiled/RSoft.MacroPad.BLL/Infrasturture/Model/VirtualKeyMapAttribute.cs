using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x02000037 RID: 55
	[AttributeUsage(256, AllowMultiple = false)]
	public class VirtualKeyMapAttribute : Attribute
	{
		// Token: 0x1700002F RID: 47
		// (get) Token: 0x060000CD RID: 205 RVA: 0x0000403D File Offset: 0x0000223D
		public VirtualKey Key { get; }

		// Token: 0x060000CE RID: 206 RVA: 0x00004045 File Offset: 0x00002245
		public VirtualKeyMapAttribute(VirtualKey key)
		{
			this.Key = key;
		}
	}
}
