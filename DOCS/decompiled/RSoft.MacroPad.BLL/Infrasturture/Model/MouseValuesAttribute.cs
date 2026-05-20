using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x02000034 RID: 52
	[AttributeUsage(256, AllowMultiple = true)]
	public class MouseValuesAttribute : Attribute
	{
		// Token: 0x1700002D RID: 45
		// (get) Token: 0x060000CA RID: 202 RVA: 0x00004017 File Offset: 0x00002217
		public byte Buttons { get; }

		// Token: 0x1700002E RID: 46
		// (get) Token: 0x060000CB RID: 203 RVA: 0x0000401F File Offset: 0x0000221F
		public byte Scroll { get; }

		// Token: 0x060000CC RID: 204 RVA: 0x00004027 File Offset: 0x00002227
		public MouseValuesAttribute(byte buttons, byte scroll)
		{
			this.Buttons = buttons;
			this.Scroll = scroll;
		}
	}
}
