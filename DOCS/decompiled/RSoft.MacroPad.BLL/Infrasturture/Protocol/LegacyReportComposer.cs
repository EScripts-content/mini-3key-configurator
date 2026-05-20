using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol.Legacy;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol
{
	// Token: 0x02000017 RID: 23
	public class LegacyReportComposer : ReportComposerBase, IReportComposer
	{
		// Token: 0x0600007D RID: 125 RVA: 0x000030AD File Offset: 0x000012AD
		public LegacyReportComposer(byte reportId)
			: base(reportId)
		{
		}

		// Token: 0x0600007E RID: 126 RVA: 0x000030B8 File Offset: 0x000012B8
		private List<Report> KeyFunctionInit(byte layerNo)
		{
			List<Report> list = new List<Report>();
			if (base.ReportId != 0)
			{
				list.Add(LayerSelectionReport.Create(base.ReportId, layerNo));
			}
			return list;
		}

		// Token: 0x0600007F RID: 127 RVA: 0x000030E6 File Offset: 0x000012E6
		private List<Report> KeyFunctionEnd(List<Report> reports)
		{
			reports.Add(WriteFlashReport.Create(base.ReportId, false));
			return reports;
		}

		// Token: 0x06000080 RID: 128 RVA: 0x000030FC File Offset: 0x000012FC
		public IEnumerable<Report> Key(InputAction action, byte layerNo, ushort delay, [TupleElementNames(new string[] { "Key", "Modifiers" })] IEnumerable<ValueTuple<KeyCode, Modifier>> sequence)
		{
			if (Enumerable.Count<ValueTuple<KeyCode, Modifier>>(sequence) == 0)
			{
				sequence = new ValueTuple<KeyCode, Modifier>[]
				{
					new ValueTuple<KeyCode, Modifier>(KeyCode.None, Modifier.None)
				};
			}
			List<Report> list = this.KeyFunctionInit(layerNo);
			list.AddRange(KeyFunctionReport.Create(base.ReportId, action, layerNo, sequence));
			return this.KeyFunctionEnd(list);
		}

		// Token: 0x06000081 RID: 129 RVA: 0x0000314C File Offset: 0x0000134C
		public IEnumerable<Report> Media(InputAction action, byte layerNo, MediaKey key)
		{
			List<Report> list = this.KeyFunctionInit(layerNo);
			list.Add(KeyFunctionReport.CreateMultimedia(base.ReportId, action, layerNo, key));
			return this.KeyFunctionEnd(list);
		}

		// Token: 0x06000082 RID: 130 RVA: 0x0000317C File Offset: 0x0000137C
		public IEnumerable<Report> Mouse(InputAction action, byte layerNo, MouseButton func, Modifier modifiers)
		{
			List<Report> list = this.KeyFunctionInit(layerNo);
			list.Add(MouseFunctionReport.Create(base.ReportId, action, layerNo, func, modifiers));
			return this.KeyFunctionEnd(list);
		}

		// Token: 0x06000083 RID: 131 RVA: 0x000031B0 File Offset: 0x000013B0
		public IEnumerable<Report> Led(byte layerNo, LedMode mode, LedColor color)
		{
			List<Report> list = new List<Report>();
			if (mode > LedMode.Mode2 && base.ReportId == 0)
			{
				return list;
			}
			list.Add(LedFunctionReport.Create(base.ReportId, mode, color));
			list.Add(WriteFlashReport.Create(base.ReportId, true));
			return list;
		}
	}
}
