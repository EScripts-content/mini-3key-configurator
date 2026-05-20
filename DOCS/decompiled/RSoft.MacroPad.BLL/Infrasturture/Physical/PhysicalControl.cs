using System;
using System.Collections.Generic;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Physical
{
	// Token: 0x02000027 RID: 39
	public abstract class PhysicalControl
	{
		// Token: 0x17000023 RID: 35
		// (get) Token: 0x060000B7 RID: 183
		public abstract ControlType Type { get; }

		// Token: 0x17000024 RID: 36
		// (get) Token: 0x060000B8 RID: 184 RVA: 0x00003F0C File Offset: 0x0000210C
		// (set) Token: 0x060000B9 RID: 185 RVA: 0x00003F14 File Offset: 0x00002114
		public virtual Vector Size { get; set; }

		// Token: 0x17000025 RID: 37
		// (get) Token: 0x060000BA RID: 186 RVA: 0x00003F1D File Offset: 0x0000211D
		// (set) Token: 0x060000BB RID: 187 RVA: 0x00003F25 File Offset: 0x00002125
		public virtual Vector Position { get; set; }

		// Token: 0x17000026 RID: 38
		// (get) Token: 0x060000BC RID: 188 RVA: 0x00003F2E File Offset: 0x0000212E
		// (set) Token: 0x060000BD RID: 189 RVA: 0x00003F36 File Offset: 0x00002136
		public string Name { get; set; }

		// Token: 0x17000027 RID: 39
		// (get) Token: 0x060000BE RID: 190 RVA: 0x00003F3F File Offset: 0x0000213F
		// (set) Token: 0x060000BF RID: 191 RVA: 0x00003F47 File Offset: 0x00002147
		public IEnumerable<InputAction> Actions { get; protected set; }
	}
}
