using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Protocol.Mappers
{
	// Token: 0x0200001E RID: 30
	public static class MouseButtonMapper
	{
		// Token: 0x06000095 RID: 149 RVA: 0x00003640 File Offset: 0x00001840
		static MouseButtonMapper()
		{
			foreach (FieldInfo fieldInfo in typeof(MouseButton).GetFields(24))
			{
				MouseButton mouseButton = (MouseButton)fieldInfo.GetValue(null);
				VirtualKeyMapAttribute customAttribute = CustomAttributeExtensions.GetCustomAttribute<VirtualKeyMapAttribute>(fieldInfo);
				MouseButtonMapper._map.Add(new ValueTuple<MouseButton, VirtualKey>(mouseButton, customAttribute.Key));
				MouseValuesAttribute customAttribute2 = CustomAttributeExtensions.GetCustomAttribute<MouseValuesAttribute>(fieldInfo);
				MouseButtonMapper._byteMap.Add(new ValueTuple<MouseButton, byte, byte>(mouseButton, customAttribute2.Buttons, customAttribute2.Scroll));
			}
		}

		// Token: 0x06000096 RID: 150 RVA: 0x000036D4 File Offset: 0x000018D4
		public static byte Button(this MouseButton key)
		{
			return Enumerable.First<ValueTuple<MouseButton, byte, byte>>(MouseButtonMapper._byteMap, ([TupleElementNames(new string[] { "Key", "Button", "Scroll" })] ValueTuple<MouseButton, byte, byte> kvp) => kvp.Item1 == key).Item2;
		}

		// Token: 0x06000097 RID: 151 RVA: 0x0000370C File Offset: 0x0000190C
		public static byte Scroll(this MouseButton key)
		{
			return Enumerable.First<ValueTuple<MouseButton, byte, byte>>(MouseButtonMapper._byteMap, ([TupleElementNames(new string[] { "Key", "Button", "Scroll" })] ValueTuple<MouseButton, byte, byte> kvp) => kvp.Item1 == key).Item3;
		}

		// Token: 0x0400004F RID: 79
		[TupleElementNames(new string[] { "Key", "Value" })]
		private static readonly List<ValueTuple<MouseButton, VirtualKey>> _map = new List<ValueTuple<MouseButton, VirtualKey>>();

		// Token: 0x04000050 RID: 80
		[TupleElementNames(new string[] { "Key", "Button", "Scroll" })]
		private static readonly List<ValueTuple<MouseButton, byte, byte>> _byteMap = new List<ValueTuple<MouseButton, byte, byte>>();
	}
}
