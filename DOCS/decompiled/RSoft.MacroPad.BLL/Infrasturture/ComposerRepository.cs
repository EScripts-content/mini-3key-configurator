using System;
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using RSoft.MacroPad.BLL.Infrasturture.Model;
using RSoft.MacroPad.BLL.Infrasturture.Protocol;

namespace RSoft.MacroPad.BLL.Infrasturture
{
	// Token: 0x0200000C RID: 12
	public class ComposerRepository
	{
		// Token: 0x0600002C RID: 44 RVA: 0x0000275E File Offset: 0x0000095E
		public ComposerRepository()
		{
			this._cache = new List<ValueTuple<IReportComposer, ProtocolType, byte>>();
		}

		// Token: 0x0600002D RID: 45 RVA: 0x00002774 File Offset: 0x00000974
		public IReportComposer Get(ProtocolType type, byte version)
		{
			int num = this._cache.FindIndex(([TupleElementNames(new string[] { "Composer", "Type", "Version" })] ValueTuple<IReportComposer, ProtocolType, byte> x) => x.Item2 == type && x.Item3 == version);
			if (num != -1)
			{
				return this._cache[num].Item1;
			}
			IReportComposer reportComposer2;
			if (type != ProtocolType.Legacy)
			{
				IReportComposer reportComposer = new ExtendedReportComposer(version);
				reportComposer2 = reportComposer;
			}
			else
			{
				IReportComposer reportComposer = new LegacyReportComposer(version);
				reportComposer2 = reportComposer;
			}
			IReportComposer reportComposer3 = reportComposer2;
			this._cache.Add(new ValueTuple<IReportComposer, ProtocolType, byte>(reportComposer3, type, version));
			return reportComposer3;
		}

		// Token: 0x04000036 RID: 54
		[TupleElementNames(new string[] { "Composer", "Type", "Version" })]
		public List<ValueTuple<IReportComposer, ProtocolType, byte>> _cache;
	}
}
