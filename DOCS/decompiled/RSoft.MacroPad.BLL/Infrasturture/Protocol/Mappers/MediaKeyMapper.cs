using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers
{
	// Token: 0x0200001C RID: 28
	public static class MediaKeyMapper
	{
		// Token: 0x0600008F RID: 143 RVA: 0x00003408 File Offset: 0x00001608
		static MediaKeyMapper()
		{
			foreach (FieldInfo fieldInfo in typeof(MediaKey).GetFields(24))
			{
				MediaKey mediaKey = (MediaKey)fieldInfo.GetValue(null);
				VirtualKeyMapAttribute customAttribute = CustomAttributeExtensions.GetCustomAttribute<VirtualKeyMapAttribute>(fieldInfo);
				MediaKeyMapper._map.Add(new ValueTuple<MediaKey, VirtualKey>(mediaKey, customAttribute.Key));
				IEnumerable<MediaValueAttribute> customAttributes = CustomAttributeExtensions.GetCustomAttributes<MediaValueAttribute>(fieldInfo);
				int[] array = new int[]
				{
					default(int),
					2,
					3
				};
				for (int j = 0; j < array.Length; j++)
				{
					int v = array[j];
					MediaValueAttribute mediaValueAttribute = Enumerable.FirstOrDefault<MediaValueAttribute>(customAttributes, (MediaValueAttribute a) => (int)a.Version == v);
					MediaKeyMapper._byteMap.Add(new ValueTuple<MediaKey, byte, byte, byte>(mediaKey, (byte)v, (mediaValueAttribute != null) ? mediaValueAttribute.B1 : 0, (mediaValueAttribute != null) ? mediaValueAttribute.B2 : 0));
				}
			}
		}

		// Token: 0x06000090 RID: 144 RVA: 0x00003504 File Offset: 0x00001704
		public static MediaKey Map(this VirtualKey key)
		{
			return Enumerable.First<ValueTuple<MediaKey, VirtualKey>>(MediaKeyMapper._map, ([TupleElementNames(new string[] { "Key", "Value" })] ValueTuple<MediaKey, VirtualKey> kvp) => kvp.Item2 == key).Item1;
		}

		// Token: 0x06000091 RID: 145 RVA: 0x0000353C File Offset: 0x0000173C
		public static VirtualKey Map(this MediaKey key)
		{
			return Enumerable.First<ValueTuple<MediaKey, VirtualKey>>(MediaKeyMapper._map, ([TupleElementNames(new string[] { "Key", "Value" })] ValueTuple<MediaKey, VirtualKey> kvp) => kvp.Item1 == key).Item2;
		}

		// Token: 0x06000092 RID: 146 RVA: 0x00003574 File Offset: 0x00001774
		public static byte B1(this MediaKey key, byte version)
		{
			return Enumerable.First<ValueTuple<MediaKey, byte, byte, byte>>(MediaKeyMapper._byteMap, ([TupleElementNames(new string[] { "Key", "Version", "B1", "B2" })] ValueTuple<MediaKey, byte, byte, byte> kvp) => kvp.Item1 == key && kvp.Item2 == version).Item3;
		}

		// Token: 0x06000093 RID: 147 RVA: 0x000035B0 File Offset: 0x000017B0
		public static byte B2(this MediaKey key, byte version)
		{
			return Enumerable.First<ValueTuple<MediaKey, byte, byte, byte>>(MediaKeyMapper._byteMap, ([TupleElementNames(new string[] { "Key", "Version", "B1", "B2" })] ValueTuple<MediaKey, byte, byte, byte> kvp) => kvp.Item1 == key && kvp.Item2 == version).Item4;
		}

		// Token: 0x0400004D RID: 77
		[TupleElementNames(new string[] { "Key", "Value" })]
		private static readonly List<ValueTuple<MediaKey, VirtualKey>> _map = new List<ValueTuple<MediaKey, VirtualKey>>();

		// Token: 0x0400004E RID: 78
		[TupleElementNames(new string[] { "Key", "Version", "B1", "B2" })]
		private static readonly List<ValueTuple<MediaKey, byte, byte, byte>> _byteMap = new List<ValueTuple<MediaKey, byte, byte, byte>>();
	}
}
