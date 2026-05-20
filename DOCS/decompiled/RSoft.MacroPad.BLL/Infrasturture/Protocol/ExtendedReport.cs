using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol
{
	// Token: 0x02000013 RID: 19
	internal class ExtendedReport : Report
	{
		// Token: 0x0600006C RID: 108 RVA: 0x00002E5F File Offset: 0x0000105F
		private ExtendedReport()
		{
		}

		// Token: 0x0600006D RID: 109 RVA: 0x00002E68 File Offset: 0x00001068
		public static ExtendedReport CreateKey(byte reportId, InputAction action, byte layerNo, [TupleElementNames(new string[] { "Key", "Modifiers" })] IEnumerable<ValueTuple<KeyCode, Modifier>> sequence, ushort delay)
		{
			byte[] array = new byte[Enumerable.Count<ValueTuple<KeyCode, Modifier>>(sequence) * 2];
			int num = 0;
			foreach (ValueTuple<KeyCode, Modifier> valueTuple in sequence)
			{
				KeyCode item = valueTuple.Item1;
				Modifier item2 = valueTuple.Item2;
				array[num++] = (byte)item2;
				array[num++] = (byte)item;
			}
			return ExtendedReport.Create(reportId, action, layerNo, delay, KeyType.Basic, array);
		}

		// Token: 0x0600006E RID: 110 RVA: 0x00002EE4 File Offset: 0x000010E4
		public static ExtendedReport CreateMedia(byte reportId, InputAction action, byte layerNo, MediaKey key)
		{
			return ExtendedReport.Create(reportId, action, layerNo, 0, KeyType.Multimedia, new byte[]
			{
				0,
				key.B1(reportId),
				key.B2(reportId),
				0
			});
		}

		// Token: 0x0600006F RID: 111 RVA: 0x00002F20 File Offset: 0x00001120
		public static ExtendedReport CreateMouse(byte reportId, InputAction action, byte layerNo, MouseButton b, Modifier modifiers)
		{
			return ExtendedReport.Create(reportId, action, layerNo, 0, KeyType.Multimedia, new byte[]
			{
				b.Button(),
				0,
				0,
				b.Scroll(),
				(byte)modifiers,
				0
			});
		}

		// Token: 0x06000070 RID: 112 RVA: 0x00002F64 File Offset: 0x00001164
		public static ExtendedReport CreateLed(byte reportId, byte layerNo, LedMode mode, LedColor color)
		{
			byte[] array = new byte[6];
			array[0] = layerNo;
			array[1] = (byte)(mode | (LedMode)color);
			return ExtendedReport.Create(reportId, (InputAction)176, layerNo, 0, KeyType.LED, array);
		}

		// Token: 0x06000071 RID: 113 RVA: 0x00002F94 File Offset: 0x00001194
		private static ExtendedReport Create(byte reportId, InputAction action, byte layerNo, ushort delay, KeyType keyType, byte[] data)
		{
			ExtendedReport extendedReport = new ExtendedReport();
			extendedReport.ReportId = reportId;
			extendedReport.Data[0] = 254;
			extendedReport.Data[1] = action.MapToByte();
			extendedReport.Data[2] = layerNo;
			extendedReport.Data[3] = (byte)keyType;
			extendedReport.Data[4] = (byte)(delay & 255);
			extendedReport.Data[5] = (byte)((delay >> 8) & 255);
			extendedReport.Data[6] = 0;
			extendedReport.Data[7] = 0;
			extendedReport.Data[8] = 0;
			byte b = 0;
			int num = 0;
			while (num < data.Length && num < extendedReport.Data.Length - 10)
			{
				extendedReport.Data[10 + num] = data[num];
				if (data[num] != 0)
				{
					b = (byte)((num >> 1) + 1);
				}
				num++;
			}
			extendedReport.Data[9] = b;
			return extendedReport;
		}
	}
}
