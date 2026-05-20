using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol
{
	// Token: 0x02000019 RID: 25
	public class VersionCheckReport : Report
	{
		// Token: 0x06000089 RID: 137 RVA: 0x00003268 File Offset: 0x00001468
		private VersionCheckReport()
		{
		}

		// Token: 0x0600008A RID: 138 RVA: 0x00003270 File Offset: 0x00001470
		public static VersionCheckReport Create(byte version)
		{
			VersionCheckReport versionCheckReport = new VersionCheckReport();
			versionCheckReport.ReportId = version;
			versionCheckReport.Data[0] = 0;
			versionCheckReport.Data[1] = 0;
			return versionCheckReport;
		}
	}
}
