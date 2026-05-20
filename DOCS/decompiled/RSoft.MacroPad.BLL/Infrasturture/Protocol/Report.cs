using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol
{
	// Token: 0x02000014 RID: 20
	public class Report
	{
		// Token: 0x17000018 RID: 24
		// (get) Token: 0x06000072 RID: 114 RVA: 0x0000305F File Offset: 0x0000125F
		// (set) Token: 0x06000073 RID: 115 RVA: 0x00003067 File Offset: 0x00001267
		public virtual byte ReportId { get; protected set; }

		// Token: 0x17000019 RID: 25
		// (get) Token: 0x06000074 RID: 116 RVA: 0x00003070 File Offset: 0x00001270
		// (set) Token: 0x06000075 RID: 117 RVA: 0x00003078 File Offset: 0x00001278
		public virtual byte[] Data { get; protected set; } = new byte[65];
	}
}
