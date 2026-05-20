using System;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers
{
	// Token: 0x0200001A RID: 26
	internal static class InputActionMapper
	{
		// Token: 0x0600008B RID: 139 RVA: 0x00003290 File Offset: 0x00001490
		public static byte MapToByte(this InputAction action)
		{
			if (action - InputAction.Key1 <= 11)
			{
				return (byte)action;
			}
			if (action - InputAction.Knob1Left > 8)
			{
				return 0;
			}
			return action - InputAction.Key10;
		}
	}
}
