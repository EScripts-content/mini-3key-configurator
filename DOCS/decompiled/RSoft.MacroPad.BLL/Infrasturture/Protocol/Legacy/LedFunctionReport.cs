using System;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Legacy
{
	// Token: 0x02000021 RID: 33
	internal class LedFunctionReport : Report
	{
		// Token: 0x0600009D RID: 157 RVA: 0x000038C6 File Offset: 0x00001AC6
		private LedFunctionReport()
		{
		}

		// Token: 0x0600009E RID: 158 RVA: 0x000038CE File Offset: 0x00001ACE
		public static LedFunctionReport Create(byte reportId, LedMode mode, LedColor color)
		{
			LedFunctionReport ledFunctionReport = new LedFunctionReport();
			ledFunctionReport.ReportId = reportId;
			ledFunctionReport.Data[0] = 176;
			ledFunctionReport.Data[1] = 8;
			ledFunctionReport.Data[2] = (byte)(mode | (LedMode)color);
			return ledFunctionReport;
		}
	}
}
