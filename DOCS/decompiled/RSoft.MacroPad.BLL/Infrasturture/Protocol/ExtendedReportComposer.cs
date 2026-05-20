using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol
{
	// Token: 0x02000018 RID: 24
	public class ExtendedReportComposer : ReportComposerBase, IReportComposer
	{
		// Token: 0x06000084 RID: 132 RVA: 0x000031F7 File Offset: 0x000013F7
		public ExtendedReportComposer(byte reportId)
			: base(reportId)
		{
		}

		// Token: 0x06000085 RID: 133 RVA: 0x00003200 File Offset: 0x00001400
		public IEnumerable<Report> Key(InputAction action, byte layerNo, ushort delay, [TupleElementNames(new string[] { "Key", "Modifiers" })] IEnumerable<ValueTuple<KeyCode, Modifier>> sequence)
		{
			return new ExtendedReport[] { ExtendedReport.CreateKey(base.ReportId, action, layerNo, sequence, delay) };
		}

		// Token: 0x06000086 RID: 134 RVA: 0x0000321B File Offset: 0x0000141B
		public IEnumerable<Report> Led(byte layerNo, LedMode mode, LedColor color)
		{
			return new ExtendedReport[] { ExtendedReport.CreateLed(base.ReportId, layerNo, mode, color) };
		}

		// Token: 0x06000087 RID: 135 RVA: 0x00003234 File Offset: 0x00001434
		public IEnumerable<Report> Media(InputAction action, byte layerNo, MediaKey key)
		{
			return new ExtendedReport[] { ExtendedReport.CreateMedia(base.ReportId, action, layerNo, key) };
		}

		// Token: 0x06000088 RID: 136 RVA: 0x0000324D File Offset: 0x0000144D
		public IEnumerable<Report> Mouse(InputAction action, byte layerNo, MouseButton func, Modifier modifiers)
		{
			return new ExtendedReport[] { ExtendedReport.CreateMouse(base.ReportId, action, layerNo, func, modifiers) };
		}
	}
}
