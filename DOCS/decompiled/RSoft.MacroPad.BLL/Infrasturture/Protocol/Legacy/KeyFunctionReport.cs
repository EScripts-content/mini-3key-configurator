using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Legacy
{
	// Token: 0x0200001F RID: 31
	internal class KeyFunctionReport : Report
	{
		// Token: 0x06000098 RID: 152 RVA: 0x00003741 File Offset: 0x00001941
		private KeyFunctionReport()
		{
		}

		// Token: 0x06000099 RID: 153 RVA: 0x0000374C File Offset: 0x0000194C
		public static KeyFunctionReport[] Create(byte reportId, InputAction action, byte layerNo, [TupleElementNames(new string[] { "Key", "Modifiers" })] IEnumerable<ValueTuple<KeyCode, Modifier>> keySequence)
		{
			ValueTuple<KeyCode, Modifier>[] array = Enumerable.ToArray<ValueTuple<KeyCode, Modifier>>(keySequence);
			KeyFunctionReport[] array2 = new KeyFunctionReport[array.Length + 1];
			byte b = 0;
			while ((int)b <= array.Length)
			{
				KeyFunctionReport keyFunctionReport = new KeyFunctionReport();
				keyFunctionReport.ReportId = reportId;
				keyFunctionReport.Data[0] = action.MapToByte();
				keyFunctionReport.Data[1] = 1;
				if (reportId != 0)
				{
					byte[] data = keyFunctionReport.Data;
					int num = 1;
					data[num] |= (byte)(((int)layerNo << 4) & 255);
				}
				keyFunctionReport.Data[2] = (byte)array.Length;
				keyFunctionReport.Data[3] = b;
				if (b == 0)
				{
					keyFunctionReport.Data[4] = (byte)array[0].Item2;
					keyFunctionReport.Data[5] = 0;
				}
				else
				{
					keyFunctionReport.Data[4] = (byte)array[(int)(b - 1)].Item2;
					keyFunctionReport.Data[5] = (byte)array[(int)(b - 1)].Item1;
				}
				array2[(int)b] = keyFunctionReport;
				b += 1;
			}
			return array2;
		}

		// Token: 0x0600009A RID: 154 RVA: 0x0000382C File Offset: 0x00001A2C
		public static KeyFunctionReport CreateMultimedia(byte reportId, InputAction action, byte layerNo, MediaKey key)
		{
			KeyFunctionReport keyFunctionReport = new KeyFunctionReport();
			keyFunctionReport.ReportId = reportId;
			keyFunctionReport.Data[0] = action.MapToByte();
			keyFunctionReport.Data[1] = 2;
			if (reportId != 0)
			{
				byte[] data = keyFunctionReport.Data;
				int num = 1;
				data[num] |= (byte)(((int)layerNo << 4) & 255);
			}
			keyFunctionReport.Data[2] = key.B1(reportId);
			keyFunctionReport.Data[3] = key.B2(reportId);
			return keyFunctionReport;
		}
	}
}
