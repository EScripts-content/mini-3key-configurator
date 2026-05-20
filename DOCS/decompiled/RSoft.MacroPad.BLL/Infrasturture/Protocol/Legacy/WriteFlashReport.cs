using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Legacy
{
	// Token: 0x02000023 RID: 35
	internal class WriteFlashReport : Report
	{
		// Token: 0x060000A1 RID: 161 RVA: 0x00003990 File Offset: 0x00001B90
		private WriteFlashReport()
		{
		}

		// Token: 0x060000A2 RID: 162 RVA: 0x00003998 File Offset: 0x00001B98
		public static WriteFlashReport Create(byte reportId, bool led = false)
		{
			WriteFlashReport writeFlashReport = new WriteFlashReport();
			writeFlashReport.ReportId = reportId;
			writeFlashReport.Data[0] = 170;
			writeFlashReport.Data[1] = (led ? 161 : 170);
			return writeFlashReport;
		}
	}
}
