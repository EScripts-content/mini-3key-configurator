using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;

namespace RSoft.MacroPad.BLL
{
	// Token: 0x0200000A RID: 10
	public static class HidLog
	{
		// Token: 0x06000027 RID: 39 RVA: 0x00002697 File Offset: 0x00000897
		public static void ClearLog()
		{
			File.WriteAllText("hid.log", "");
		}

		// Token: 0x06000028 RID: 40 RVA: 0x000026A8 File Offset: 0x000008A8
		public static void AppendMsg(byte reportId, IEnumerable<byte> data)
		{
			string text = "hid.log";
			DefaultInterpolatedStringHandler defaultInterpolatedStringHandler;
			defaultInterpolatedStringHandler..ctor(2, 1);
			defaultInterpolatedStringHandler.AppendFormatted<byte>(reportId);
			defaultInterpolatedStringHandler.AppendLiteral("\n\n");
			File.AppendAllText(text, defaultInterpolatedStringHandler.ToStringAndClear());
			File.AppendAllText("hid.log", string.Join<byte>("\n", data));
			File.AppendAllText("hid.log", "\n------\n");
		}

		// Token: 0x04000034 RID: 52
		private const string FILE = "hid.log";
	}
}
