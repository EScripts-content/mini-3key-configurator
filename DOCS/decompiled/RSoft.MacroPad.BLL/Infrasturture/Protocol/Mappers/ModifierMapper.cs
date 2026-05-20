using System;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers
{
	// Token: 0x0200001D RID: 29
	public static class ModifierMapper
	{
		// Token: 0x06000094 RID: 148 RVA: 0x000035EC File Offset: 0x000017EC
		public static Modifier Map(bool lShft, bool rShft, bool lAlt, bool rAlt, bool lCtrl, bool rCtrl, bool lWin, bool rWin)
		{
			Modifier modifier = Modifier.None;
			if (lShft)
			{
				modifier |= Modifier.Shift;
			}
			if (rShft)
			{
				modifier |= Modifier.RightShift;
			}
			if (lAlt)
			{
				modifier |= Modifier.Alt;
			}
			if (rAlt)
			{
				modifier |= Modifier.RightAlt;
			}
			if (lCtrl)
			{
				modifier |= Modifier.Ctrl;
			}
			if (rCtrl)
			{
				modifier |= Modifier.RightCtrl;
			}
			if (lWin)
			{
				modifier |= Modifier.Win;
			}
			if (rWin)
			{
				modifier |= Modifier.RightWin;
			}
			return modifier;
		}
	}
}
