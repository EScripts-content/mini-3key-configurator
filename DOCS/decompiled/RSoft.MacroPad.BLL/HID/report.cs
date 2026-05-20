using System;

namespace HID
{
	// Token: 0x02000006 RID: 6
	public class report : EventArgs
	{
		// Token: 0x06000025 RID: 37 RVA: 0x00002659 File Offset: 0x00000859
		public report(byte id, byte[] arrayBuff)
		{
			this.reportID = id;
			this.reportBuff = arrayBuff;
		}

		// Token: 0x04000028 RID: 40
		public readonly byte reportID;

		// Token: 0x04000029 RID: 41
		public readonly byte[] reportBuff;
	}
}
