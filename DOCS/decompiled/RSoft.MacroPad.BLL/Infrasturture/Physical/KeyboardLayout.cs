using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;

namespace RSoft.MacroPad.BLL.Infrasturture.Physical
{
	// Token: 0x02000025 RID: 37
	public class KeyboardLayout
	{
		// Token: 0x1700001B RID: 27
		// (get) Token: 0x060000A3 RID: 163 RVA: 0x000039CB File Offset: 0x00001BCB
		// (set) Token: 0x060000A4 RID: 164 RVA: 0x000039D3 File Offset: 0x00001BD3
		public string Name { get; set; }

		// Token: 0x1700001C RID: 28
		// (get) Token: 0x060000A5 RID: 165 RVA: 0x000039DC File Offset: 0x00001BDC
		// (set) Token: 0x060000A6 RID: 166 RVA: 0x000039E4 File Offset: 0x00001BE4
		[TupleElementNames(new string[] { "VendorId", "ProductId" })]
		public IEnumerable<ValueTuple<ushort, ushort>> Products
		{
			[return: TupleElementNames(new string[] { "VendorId", "ProductId" })]
			get;
			[param: TupleElementNames(new string[] { "VendorId", "ProductId" })]
			set;
		}

		// Token: 0x1700001D RID: 29
		// (get) Token: 0x060000A7 RID: 167 RVA: 0x000039ED File Offset: 0x00001BED
		// (set) Token: 0x060000A8 RID: 168 RVA: 0x000039F5 File Offset: 0x00001BF5
		public byte LayerCount { get; set; }

		// Token: 0x1700001E RID: 30
		// (get) Token: 0x060000A9 RID: 169 RVA: 0x000039FE File Offset: 0x00001BFE
		// (set) Token: 0x060000AA RID: 170 RVA: 0x00003A06 File Offset: 0x00001C06
		public byte MaxCharacters { get; set; }

		// Token: 0x1700001F RID: 31
		// (get) Token: 0x060000AB RID: 171 RVA: 0x00003A0F File Offset: 0x00001C0F
		// (set) Token: 0x060000AC RID: 172 RVA: 0x00003A17 File Offset: 0x00001C17
		public bool SupportsDelay { get; set; }

		// Token: 0x17000020 RID: 32
		// (get) Token: 0x060000AD RID: 173 RVA: 0x00003A20 File Offset: 0x00001C20
		// (set) Token: 0x060000AE RID: 174 RVA: 0x00003A28 File Offset: 0x00001C28
		public bool SupportsColor { get; set; }

		// Token: 0x17000021 RID: 33
		// (get) Token: 0x060000AF RID: 175 RVA: 0x00003A31 File Offset: 0x00001C31
		// (set) Token: 0x060000B0 RID: 176 RVA: 0x00003A39 File Offset: 0x00001C39
		public byte LedModeCount { get; set; }

		// Token: 0x17000022 RID: 34
		// (get) Token: 0x060000B1 RID: 177 RVA: 0x00003A42 File Offset: 0x00001C42
		// (set) Token: 0x060000B2 RID: 178 RVA: 0x00003A4A File Offset: 0x00001C4A
		public IEnumerable<PhysicalControl> Controls { get; set; }

		// Token: 0x060000B3 RID: 179 RVA: 0x00003A54 File Offset: 0x00001C54
		public override string ToString()
		{
			DefaultInterpolatedStringHandler defaultInterpolatedStringHandler;
			defaultInterpolatedStringHandler..ctor(34, 4);
			defaultInterpolatedStringHandler.AppendFormatted(this.Name);
			defaultInterpolatedStringHandler.AppendLiteral(" (");
			defaultInterpolatedStringHandler.AppendFormatted<int>(Enumerable.Count<PhysicalControl>(this.Controls, (PhysicalControl c) => c is PhysicalButton));
			defaultInterpolatedStringHandler.AppendLiteral(" button(s), ");
			defaultInterpolatedStringHandler.AppendFormatted<int>(Enumerable.Count<PhysicalControl>(this.Controls, (PhysicalControl c) => c is PhysicalKnob));
			defaultInterpolatedStringHandler.AppendLiteral(" knob(s), ");
			defaultInterpolatedStringHandler.AppendFormatted<byte>(this.LayerCount);
			defaultInterpolatedStringHandler.AppendLiteral(" layer(s))");
			return defaultInterpolatedStringHandler.ToStringAndClear();
		}
	}
}
