using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Runtime.CompilerServices;

namespace RSoft.MacroPad.BLL.Infrasturture.Physical
{
	// Token: 0x02000026 RID: 38
	public class LayoutParser
	{
		// Token: 0x060000B5 RID: 181 RVA: 0x00003B28 File Offset: 0x00001D28
		public KeyboardLayout[] Parse(string path)
		{
			string[] array = Enumerable.ToArray<string>(Enumerable.Select<string, string>(File.ReadAllLines(path), (string l) => l.Trim()));
			KeyboardLayout keyboardLayout = null;
			List<KeyboardLayout> list = new List<KeyboardLayout>();
			int num = 0;
			for (int j = 0; j < array.Length; j++)
			{
				num++;
				string text = array[j];
				if (!string.IsNullOrEmpty(text) && !text.StartsWith("//"))
				{
					try
					{
						if (text.StartsWith("Layout:"))
						{
							keyboardLayout = new KeyboardLayout();
							keyboardLayout.Name = text.Substring(7);
							IEnumerable<string> enumerable = array[++j].Trim().Split(',', 0);
							List<ValueTuple<ushort, ushort>> list2 = new List<ValueTuple<ushort, ushort>>();
							foreach (string[] array2 in Enumerable.Select<string, string[]>(enumerable, (string i) => i.Split(':', 0)))
							{
								list2.Add(new ValueTuple<ushort, ushort>(ushort.Parse(array2[0].Trim()), ushort.Parse(array2[1].Trim())));
							}
							keyboardLayout.Products = list2;
							string[] array3 = Enumerable.ToArray<string>(Enumerable.Select<string, string>(array[++j].Split(':', 0), (string b) => b.Trim()));
							keyboardLayout.LayerCount = byte.Parse(array3[0]);
							keyboardLayout.MaxCharacters = byte.Parse(array3[1]);
							keyboardLayout.SupportsDelay = byte.Parse(array3[2]) > 0;
							keyboardLayout.SupportsColor = byte.Parse(array3[3]) > 0;
							keyboardLayout.LedModeCount = byte.Parse(array3[4]);
							keyboardLayout.Controls = new List<PhysicalControl>();
							list.Add(keyboardLayout);
							goto IL_0361;
						}
						if (text.StartsWith("B"))
						{
							string[] array4 = text.Split(',', 0);
							int num2 = int.Parse(array4[0].Substring(1));
							PhysicalButton physicalButton = new PhysicalButton(num2);
							physicalButton.Position = new Vector(int.Parse(array4[1]), int.Parse(array4[2]));
							if (array4.Length >= 5)
							{
								physicalButton.Size = new Vector(int.Parse(array4[3]), int.Parse(array4[4]));
							}
							physicalButton.Name = num2.ToString();
							((List<PhysicalControl>)keyboardLayout.Controls).Add(physicalButton);
							goto IL_0361;
						}
						if (text.StartsWith("K"))
						{
							string[] array5 = text.Split(',', 0);
							int num3 = int.Parse(array5[0].Substring(1));
							PhysicalKnob physicalKnob = new PhysicalKnob(num3);
							physicalKnob.Position = new Vector(int.Parse(array5[1]), int.Parse(array5[2]));
							if (array5.Length >= 5)
							{
								physicalKnob.Size = new Vector(int.Parse(array5[3]), int.Parse(array5[4]));
							}
							physicalKnob.Name = num3.ToString();
							((List<PhysicalControl>)keyboardLayout.Controls).Add(physicalKnob);
							goto IL_0361;
						}
					}
					catch
					{
					}
					DefaultInterpolatedStringHandler defaultInterpolatedStringHandler;
					defaultInterpolatedStringHandler..ctor(27, 3);
					defaultInterpolatedStringHandler.AppendLiteral("Invalid line format in ");
					defaultInterpolatedStringHandler.AppendFormatted(path);
					defaultInterpolatedStringHandler.AppendLiteral("(");
					defaultInterpolatedStringHandler.AppendFormatted<int>(num);
					defaultInterpolatedStringHandler.AppendLiteral("): ");
					defaultInterpolatedStringHandler.AppendFormatted(text);
					throw new InvalidDataException(defaultInterpolatedStringHandler.ToStringAndClear());
				}
				IL_0361:;
			}
			return Enumerable.ToArray<KeyboardLayout>(Enumerable.OrderBy<KeyboardLayout, string>(list, (KeyboardLayout l) => l.Name));
		}
	}
}
