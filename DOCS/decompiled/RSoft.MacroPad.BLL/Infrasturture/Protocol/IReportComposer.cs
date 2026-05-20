using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol
{
	// Token: 0x02000015 RID: 21
	public interface IReportComposer
	{
		// Token: 0x06000077 RID: 119
		IEnumerable<Report> Key(InputAction action, byte layerNo, ushort delay, [TupleElementNames(new string[] { "Key", "Modifiers" })] IEnumerable<ValueTuple<KeyCode, Modifier>> sequence);

		// Token: 0x06000078 RID: 120
		IEnumerable<Report> Media(InputAction action, byte layerNo, MediaKey key);

		// Token: 0x06000079 RID: 121
		IEnumerable<Report> Mouse(InputAction action, byte layerNo, MouseButton func, Modifier modifiers);

		// Token: 0x0600007A RID: 122
		IEnumerable<Report> Led(byte layerNo, LedMode mode, LedColor color);
	}
}
