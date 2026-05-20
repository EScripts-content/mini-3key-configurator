using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Configuration
{
	// Token: 0x02000038 RID: 56
	public class Configuration
	{
		// Token: 0x17000030 RID: 48
		// (get) Token: 0x060000CF RID: 207 RVA: 0x00004054 File Offset: 0x00002254
		// (set) Token: 0x060000D0 RID: 208 RVA: 0x0000405C File Offset: 0x0000225C
		[TupleElementNames(new string[] { "VendorId", "ProductId", "PathPattern", "ProtocolType" })]
		public IEnumerable<ValueTuple<ushort, ushort, string, ProtocolType>> SupportedDevices
		{
			[return: TupleElementNames(new string[] { "VendorId", "ProductId", "PathPattern", "ProtocolType" })]
			get;
			[param: TupleElementNames(new string[] { "VendorId", "ProductId", "PathPattern", "ProtocolType" })]
			set;
		} = new ValueTuple<ushort, ushort, string, ProtocolType>[0];
	}
}
