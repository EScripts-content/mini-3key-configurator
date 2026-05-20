using System;
using RSoft.MacroPad.BLL.Infrasturture.Model;

namespace RSoft.MacroPad.BLL.Infrasturture.Physical
{
	// Token: 0x02000029 RID: 41
	public class PhysicalKnob : PhysicalControl
	{
		// Token: 0x17000029 RID: 41
		// (get) Token: 0x060000C3 RID: 195 RVA: 0x00003F83 File Offset: 0x00002183
		public override ControlType Type
		{
			get
			{
				return ControlType.Knob;
			}
		}

		// Token: 0x060000C4 RID: 196 RVA: 0x00003F88 File Offset: 0x00002188
		public PhysicalKnob(int idx)
		{
			this.Size = new Vector(20, 20);
			int num = idx * 3 + 20;
			base.Actions = new InputAction[]
			{
				(InputAction)num,
				(InputAction)((byte)num + 1),
				(InputAction)((byte)num + 2)
			};
		}
	}
}
