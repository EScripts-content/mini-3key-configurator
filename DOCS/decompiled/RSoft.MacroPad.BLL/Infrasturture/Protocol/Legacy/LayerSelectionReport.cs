using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Legacy
{
	// Token: 0x02000020 RID: 32
	internal class LayerSelectionReport : Report
	{
		// Token: 0x0600009B RID: 155 RVA: 0x0000389A File Offset: 0x00001A9A
		private LayerSelectionReport()
		{
		}

		// Token: 0x0600009C RID: 156 RVA: 0x000038A2 File Offset: 0x00001AA2
		public static LayerSelectionReport Create(byte reportId, byte layerNo)
		{
			LayerSelectionReport layerSelectionReport = new LayerSelectionReport();
			layerSelectionReport.ReportId = reportId;
			layerSelectionReport.Data[0] = 161;
			layerSelectionReport.Data[1] = layerNo;
			return layerSelectionReport;
		}
	}
}
