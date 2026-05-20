using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text.RegularExpressions;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Configuration
{
	// Token: 0x02000039 RID: 57
	public class ConfigurationReader
	{
		// Token: 0x060000D2 RID: 210 RVA: 0x0000407C File Offset: 0x0000227C
		public Configuration Read(string fileName)
		{
			string[] array;
			try
			{
				array = Enumerable.ToArray<string>(Enumerable.Select<string, string>(File.ReadAllLines(fileName), (string l) => l.Trim()));
			}
			catch
			{
				return null;
			}
			List<ValueTuple<ushort, ushort, string, ProtocolType>> list = new List<ValueTuple<ushort, ushort, string, ProtocolType>>();
			Configuration configuration = new Configuration
			{
				SupportedDevices = list
			};
			int num = 0;
			foreach (string text in array)
			{
				num++;
				if (!string.IsNullOrEmpty(text) && !text.StartsWith("//"))
				{
					Match match = this.DeviceConfigLinePattern.Match(text);
					if (match == null || !match.Success)
					{
						DefaultInterpolatedStringHandler defaultInterpolatedStringHandler;
						defaultInterpolatedStringHandler..ctor(27, 3);
						defaultInterpolatedStringHandler.AppendLiteral("Invalid line format in ");
						defaultInterpolatedStringHandler.AppendFormatted(fileName);
						defaultInterpolatedStringHandler.AppendLiteral("(");
						defaultInterpolatedStringHandler.AppendFormatted<int>(num);
						defaultInterpolatedStringHandler.AppendLiteral("): ");
						defaultInterpolatedStringHandler.AppendFormatted(text);
						throw new InvalidDataException(defaultInterpolatedStringHandler.ToStringAndClear());
					}
					ushort num2 = ushort.Parse(match.Groups[1].Value);
					ushort num3 = ushort.Parse(match.Groups[2].Value);
					string value = match.Groups[3].Value;
					ValueTuple<ushort, ushort, string, ProtocolType> valueTuple = new ValueTuple<ushort, ushort, string, ProtocolType>(num2, num3, value, ProtocolType.Extended);
					if (match.Groups.Count > 4)
					{
						byte b = byte.Parse(match.Groups[4].Value);
						valueTuple.Item4 = ((b == 0) ? ProtocolType.Legacy : ProtocolType.Extended);
					}
					list.Add(valueTuple);
				}
			}
			return configuration;
		}

		// Token: 0x040001DA RID: 474
		private Regex DeviceConfigLinePattern = new Regex("^([0-9]+):([0-9]+),([a-zA-Z0-9\\-_]+)(?:,([01]))$");
	}
}
