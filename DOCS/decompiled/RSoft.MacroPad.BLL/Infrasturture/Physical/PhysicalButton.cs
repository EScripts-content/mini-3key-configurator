using System;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Physical
{
	// Token: 0x02000028 RID: 40
	public class PhysicalButton : PhysicalControl
	{
		// Token: 0x17000028 RID: 40
		// (get) Token: 0x060000C1 RID: 193 RVA: 0x00003F58 File Offset: 0x00002158
		public override ControlType Type
		{
			get
			{
				return ControlType.Button;
			}
		}

		// Token: 0x060000C2 RID: 194 RVA: 0x00003F5B File Offset: 0x0000215B
		public PhysicalButton(int idx)
		{
			this.Size = new Vector(20, 20);
			base.Actions = new InputAction[] { (InputAction)idx };
		}
	}
}
