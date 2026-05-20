using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers
{
	// Token: 0x0200001B RID: 27
	public static class KeyCodeMapper
	{
		// Token: 0x0600008C RID: 140 RVA: 0x000032AC File Offset: 0x000014AC
		static KeyCodeMapper()
		{
			foreach (FieldInfo fieldInfo in typeof(KeyCode).GetFields(24))
			{
				VirtualKeyMapAttribute customAttribute = CustomAttributeExtensions.GetCustomAttribute<VirtualKeyMapAttribute>(fieldInfo);
				KeyCodeMapper._map.Add(new ValueTuple<KeyCode, VirtualKey>((KeyCode)fieldInfo.GetValue(null), customAttribute.Key));
			}
			using (IEnumerator<VirtualKey> enumerator = Enumerable.Cast<VirtualKey>(Enum.GetValues(typeof(VirtualKey))).GetEnumerator())
			{
				while (enumerator.MoveNext())
				{
					VirtualKey sc = enumerator.Current;
					if (!Enumerable.Any<ValueTuple<KeyCode, VirtualKey>>(KeyCodeMapper._map, ([TupleElementNames(new string[] { "Key", "Value" })] ValueTuple<KeyCode, VirtualKey> kvp) => kvp.Item2 == sc))
					{
						KeyCodeMapper._map.Add(new ValueTuple<KeyCode, VirtualKey>(KeyCode.None, sc));
					}
				}
			}
		}

		// Token: 0x0600008D RID: 141 RVA: 0x00003398 File Offset: 0x00001598
		public static KeyCode Map(this VirtualKey key)
		{
			return Enumerable.FirstOrDefault<ValueTuple<KeyCode, VirtualKey>>(KeyCodeMapper._map, ([TupleElementNames(new string[] { "Key", "Value" })] ValueTuple<KeyCode, VirtualKey> kvp) => kvp.Item2 == key).Item1;
		}

		// Token: 0x0600008E RID: 142 RVA: 0x000033D0 File Offset: 0x000015D0
		public static VirtualKey Map(this KeyCode key)
		{
			return Enumerable.First<ValueTuple<KeyCode, VirtualKey>>(KeyCodeMapper._map, ([TupleElementNames(new string[] { "Key", "Value" })] ValueTuple<KeyCode, VirtualKey> kvp) => kvp.Item1 == key).Item2;
		}

		// Token: 0x0400004C RID: 76
		[TupleElementNames(new string[] { "Key", "Value" })]
		private static readonly List<ValueTuple<KeyCode, VirtualKey>> _map = new List<ValueTuple<KeyCode, VirtualKey>>();
	}
}
