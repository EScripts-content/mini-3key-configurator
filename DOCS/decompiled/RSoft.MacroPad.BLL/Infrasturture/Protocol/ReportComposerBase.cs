using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol
{
	// Token: 0x02000016 RID: 22
	public class ReportComposerBase
	{
		// Token: 0x1700001A RID: 26
		// (get) Token: 0x0600007B RID: 123 RVA: 0x00003096 File Offset: 0x00001296
		public byte ReportId { get; }

		// Token: 0x0600007C RID: 124 RVA: 0x0000309E File Offset: 0x0000129E
		protected ReportComposerBase(byte reportId)
		{
			this.ReportId = reportId;
		}
	}
}
