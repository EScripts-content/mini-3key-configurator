using System;
using System.Linq;
using System.Runtime.CompilerServices;

namespace RSoft.MacroPad.BLL
{
	// Token: 0x0200000B RID: 11
	public static class TestedProducts
	{
		// Token: 0x17000004 RID: 4
		// (get) Token: 0x06000029 RID: 41 RVA: 0x00002707 File Offset: 0x00000907
		[TupleElementNames(new string[] { "VendorId", "ProductId" })]
		private static ValueTuple<ushort, ushort>[] _values
		{
			[return: TupleElementNames(new string[] { "VendorId", "ProductId" })]
			get;
		} = Enumerable.ToArray<ValueTuple<ushort, ushort>>(Enumerable.Select<ValueTuple<int, int>, ValueTuple<ushort, ushort>>(new ValueTuple<int, int>[]
		{
			new ValueTuple<int, int>(4489, 34960)
		}, (ValueTuple<int, int> x) => new ValueTuple<ushort, ushort>((ushort)x.Item1, (ushort)x.Item2)));

		// Token: 0x0600002A RID: 42 RVA: 0x0000270E File Offset: 0x0000090E
		public static bool IsTested(ushort VendorId, ushort ProductId)
		{
			return Enumerable.Contains<ValueTuple<ushort, ushort>>(TestedProducts._values, new ValueTuple<ushort, ushort>(VendorId, ProductId));
		}
	}
}
