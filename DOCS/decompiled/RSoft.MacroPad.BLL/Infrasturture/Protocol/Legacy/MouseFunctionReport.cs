using System;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Legacy
{
	// Token: 0x02000022 RID: 34
	internal class MouseFunctionReport : Report
	{
		// Token: 0x0600009F RID: 159 RVA: 0x000038FE File Offset: 0x00001AFE
		private MouseFunctionReport()
		{
		}

		// Token: 0x060000A0 RID: 160 RVA: 0x00003908 File Offset: 0x00001B08
		public static MouseFunctionReport Create(byte reportId, InputAction action, byte layerNo, MouseButton button, Modifier modifiers)
		{
			MouseFunctionReport mouseFunctionReport = new MouseFunctionReport();
			mouseFunctionReport.ReportId = reportId;
			mouseFunctionReport.Data[0] = action.MapToByte();
			mouseFunctionReport.Data[1] = 3;
			if (reportId != 0)
			{
				byte[] data = mouseFunctionReport.Data;
				int num = 1;
				data[num] |= (byte)(((int)layerNo << 4) & 255);
			}
			mouseFunctionReport.Data[2] = button.Button();
			mouseFunctionReport.Data[3] = 0;
			mouseFunctionReport.Data[4] = 0;
			mouseFunctionReport.Data[5] = button.Scroll();
			mouseFunctionReport.Data[6] = (byte)modifiers;
			return mouseFunctionReport;
		}
	}
}
