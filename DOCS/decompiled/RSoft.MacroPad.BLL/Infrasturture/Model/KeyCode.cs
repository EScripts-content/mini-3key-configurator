using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x0200002C RID: 44
	public enum KeyCode : byte
	{
		// Token: 0x0400007A RID: 122
		[VirtualKeyMap(VirtualKey.A)]
		A = 4,
		// Token: 0x0400007B RID: 123
		[VirtualKeyMap(VirtualKey.B)]
		B,
		// Token: 0x0400007C RID: 124
		[VirtualKeyMap(VirtualKey.C)]
		C,
		// Token: 0x0400007D RID: 125
		[VirtualKeyMap(VirtualKey.D)]
		D,
		// Token: 0x0400007E RID: 126
		[VirtualKeyMap(VirtualKey.E)]
		E,
		// Token: 0x0400007F RID: 127
		[VirtualKeyMap(VirtualKey.F)]
		F,
		// Token: 0x04000080 RID: 128
		[VirtualKeyMap(VirtualKey.G)]
		G,
		// Token: 0x04000081 RID: 129
		[VirtualKeyMap(VirtualKey.H)]
		H,
		// Token: 0x04000082 RID: 130
		[VirtualKeyMap(VirtualKey.I)]
		I,
		// Token: 0x04000083 RID: 131
		[VirtualKeyMap(VirtualKey.J)]
		J,
		// Token: 0x04000084 RID: 132
		[VirtualKeyMap(VirtualKey.K)]
		K,
		// Token: 0x04000085 RID: 133
		[VirtualKeyMap(VirtualKey.L)]
		L,
		// Token: 0x04000086 RID: 134
		[VirtualKeyMap(VirtualKey.M)]
		M,
		// Token: 0x04000087 RID: 135
		[VirtualKeyMap(VirtualKey.N)]
		N,
		// Token: 0x04000088 RID: 136
		[VirtualKeyMap(VirtualKey.O)]
		O,
		// Token: 0x04000089 RID: 137
		[VirtualKeyMap(VirtualKey.P)]
		P,
		// Token: 0x0400008A RID: 138
		[VirtualKeyMap(VirtualKey.Q)]
		Q,
		// Token: 0x0400008B RID: 139
		[VirtualKeyMap(VirtualKey.R)]
		R,
		// Token: 0x0400008C RID: 140
		[VirtualKeyMap(VirtualKey.S)]
		S,
		// Token: 0x0400008D RID: 141
		[VirtualKeyMap(VirtualKey.T)]
		T,
		// Token: 0x0400008E RID: 142
		[VirtualKeyMap(VirtualKey.U)]
		U,
		// Token: 0x0400008F RID: 143
		[VirtualKeyMap(VirtualKey.V)]
		V,
		// Token: 0x04000090 RID: 144
		[VirtualKeyMap(VirtualKey.W)]
		W,
		// Token: 0x04000091 RID: 145
		[VirtualKeyMap(VirtualKey.X)]
		X,
		// Token: 0x04000092 RID: 146
		[VirtualKeyMap(VirtualKey.Y)]
		Y,
		// Token: 0x04000093 RID: 147
		[VirtualKeyMap(VirtualKey.Z)]
		Z,
		// Token: 0x04000094 RID: 148
		[VirtualKeyMap(VirtualKey.D1)]
		D1,
		// Token: 0x04000095 RID: 149
		[VirtualKeyMap(VirtualKey.D2)]
		D2,
		// Token: 0x04000096 RID: 150
		[VirtualKeyMap(VirtualKey.D3)]
		D3,
		// Token: 0x04000097 RID: 151
		[VirtualKeyMap(VirtualKey.D4)]
		D4,
		// Token: 0x04000098 RID: 152
		[VirtualKeyMap(VirtualKey.D5)]
		D5,
		// Token: 0x04000099 RID: 153
		[VirtualKeyMap(VirtualKey.D6)]
		D6,
		// Token: 0x0400009A RID: 154
		[VirtualKeyMap(VirtualKey.D7)]
		D7,
		// Token: 0x0400009B RID: 155
		[VirtualKeyMap(VirtualKey.D8)]
		D8,
		// Token: 0x0400009C RID: 156
		[VirtualKeyMap(VirtualKey.D9)]
		D9,
		// Token: 0x0400009D RID: 157
		[VirtualKeyMap(VirtualKey.D0)]
		D0,
		// Token: 0x0400009E RID: 158
		[VirtualKeyMap(VirtualKey.Return)]
		Enter,
		// Token: 0x0400009F RID: 159
		[VirtualKeyMap(VirtualKey.Escape)]
		Esc,
		// Token: 0x040000A0 RID: 160
		[VirtualKeyMap(VirtualKey.Back)]
		Backspace,
		// Token: 0x040000A1 RID: 161
		[VirtualKeyMap(VirtualKey.Tab)]
		Tab,
		// Token: 0x040000A2 RID: 162
		[VirtualKeyMap(VirtualKey.Space)]
		SpaceKey,
		// Token: 0x040000A3 RID: 163
		[VirtualKeyMap(VirtualKey.OemMinus)]
		Minus,
		// Token: 0x040000A4 RID: 164
		[VirtualKeyMap(VirtualKey.Oemplus)]
		Plus,
		// Token: 0x040000A5 RID: 165
		[VirtualKeyMap(VirtualKey.OemOpenBrackets)]
		OpenBracket,
		// Token: 0x040000A6 RID: 166
		[VirtualKeyMap(VirtualKey.OemCloseBrackets)]
		CloseBracket,
		// Token: 0x040000A7 RID: 167
		[VirtualKeyMap(VirtualKey.OemPipe)]
		Pipe,
		// Token: 0x040000A8 RID: 168
		[VirtualKeyMap(VirtualKey.Oemtilde)]
		Tilde = 53,
		// Token: 0x040000A9 RID: 169
		[VirtualKeyMap(VirtualKey.OemSemicolon)]
		Colon = 51,
		// Token: 0x040000AA RID: 170
		[VirtualKeyMap(VirtualKey.OemBackslash)]
		Backslash,
		// Token: 0x040000AB RID: 171
		[VirtualKeyMap(VirtualKey.Oemcomma)]
		Clear = 54,
		// Token: 0x040000AC RID: 172
		[VirtualKeyMap(VirtualKey.OemPeriod)]
		Period,
		// Token: 0x040000AD RID: 173
		[VirtualKeyMap(VirtualKey.OemQuestion)]
		Question,
		// Token: 0x040000AE RID: 174
		[VirtualKeyMap(VirtualKey.Capital)]
		CapsLock,
		// Token: 0x040000AF RID: 175
		[VirtualKeyMap(VirtualKey.F1)]
		F1,
		// Token: 0x040000B0 RID: 176
		[VirtualKeyMap(VirtualKey.F2)]
		F2,
		// Token: 0x040000B1 RID: 177
		[VirtualKeyMap(VirtualKey.F3)]
		F3,
		// Token: 0x040000B2 RID: 178
		[VirtualKeyMap(VirtualKey.F4)]
		F4,
		// Token: 0x040000B3 RID: 179
		[VirtualKeyMap(VirtualKey.F5)]
		F5,
		// Token: 0x040000B4 RID: 180
		[VirtualKeyMap(VirtualKey.F6)]
		F6,
		// Token: 0x040000B5 RID: 181
		[VirtualKeyMap(VirtualKey.F7)]
		F7,
		// Token: 0x040000B6 RID: 182
		[VirtualKeyMap(VirtualKey.F8)]
		F8,
		// Token: 0x040000B7 RID: 183
		[VirtualKeyMap(VirtualKey.F9)]
		F9,
		// Token: 0x040000B8 RID: 184
		[VirtualKeyMap(VirtualKey.F10)]
		F10,
		// Token: 0x040000B9 RID: 185
		[VirtualKeyMap(VirtualKey.F11)]
		F11,
		// Token: 0x040000BA RID: 186
		[VirtualKeyMap(VirtualKey.F12)]
		F12,
		// Token: 0x040000BB RID: 187
		[VirtualKeyMap(VirtualKey.Snapshot)]
		PrtSc,
		// Token: 0x040000BC RID: 188
		[VirtualKeyMap(VirtualKey.Scroll)]
		ScrollLock,
		// Token: 0x040000BD RID: 189
		[VirtualKeyMap(VirtualKey.Pause)]
		PauseBreak,
		// Token: 0x040000BE RID: 190
		[VirtualKeyMap(VirtualKey.Insert)]
		Insert,
		// Token: 0x040000BF RID: 191
		[VirtualKeyMap(VirtualKey.Home)]
		Home,
		// Token: 0x040000C0 RID: 192
		[VirtualKeyMap(VirtualKey.Prior)]
		PgUp,
		// Token: 0x040000C1 RID: 193
		[VirtualKeyMap(VirtualKey.Delete)]
		Del,
		// Token: 0x040000C2 RID: 194
		[VirtualKeyMap(VirtualKey.End)]
		End,
		// Token: 0x040000C3 RID: 195
		[VirtualKeyMap(VirtualKey.Next)]
		PgDn,
		// Token: 0x040000C4 RID: 196
		[VirtualKeyMap(VirtualKey.Right)]
		ArrowRight,
		// Token: 0x040000C5 RID: 197
		[VirtualKeyMap(VirtualKey.Left)]
		ArrowLeft,
		// Token: 0x040000C6 RID: 198
		[VirtualKeyMap(VirtualKey.Down)]
		ArrowDown,
		// Token: 0x040000C7 RID: 199
		[VirtualKeyMap(VirtualKey.Up)]
		ArrowUp,
		// Token: 0x040000C8 RID: 200
		[VirtualKeyMap(VirtualKey.NumLock)]
		Num,
		// Token: 0x040000C9 RID: 201
		[VirtualKeyMap(VirtualKey.Divide)]
		NumDiv,
		// Token: 0x040000CA RID: 202
		[VirtualKeyMap(VirtualKey.Multiply)]
		NumMul,
		// Token: 0x040000CB RID: 203
		[VirtualKeyMap(VirtualKey.Subtract)]
		NumSub,
		// Token: 0x040000CC RID: 204
		[VirtualKeyMap(VirtualKey.Add)]
		NumAdd,
		// Token: 0x040000CD RID: 205
		[VirtualKeyMap(VirtualKey.NumPad1)]
		Num1 = 89,
		// Token: 0x040000CE RID: 206
		[VirtualKeyMap(VirtualKey.NumPad2)]
		Num2,
		// Token: 0x040000CF RID: 207
		[VirtualKeyMap(VirtualKey.NumPad3)]
		Num3,
		// Token: 0x040000D0 RID: 208
		[VirtualKeyMap(VirtualKey.NumPad4)]
		Num4,
		// Token: 0x040000D1 RID: 209
		[VirtualKeyMap(VirtualKey.NumPad5)]
		Num5,
		// Token: 0x040000D2 RID: 210
		[VirtualKeyMap(VirtualKey.NumPad6)]
		Num6,
		// Token: 0x040000D3 RID: 211
		[VirtualKeyMap(VirtualKey.NumPad7)]
		Num7,
		// Token: 0x040000D4 RID: 212
		[VirtualKeyMap(VirtualKey.NumPad8)]
		Num8,
		// Token: 0x040000D5 RID: 213
		[VirtualKeyMap(VirtualKey.NumPad9)]
		Num9,
		// Token: 0x040000D6 RID: 214
		[VirtualKeyMap(VirtualKey.NumPad0)]
		Num0,
		// Token: 0x040000D7 RID: 215
		[VirtualKeyMap(VirtualKey.Decimal)]
		NumDec,
		// Token: 0x040000D8 RID: 216
		[VirtualKeyMap(VirtualKey.Return)]
		NumEnter,
		// Token: 0x040000D9 RID: 217
		[VirtualKeyMap(VirtualKey.Apps)]
		App,
		// Token: 0x040000DA RID: 218
		[VirtualKeyMap(VirtualKey.OemPipe)]
		IsoPlus1,
		// Token: 0x040000DB RID: 219
		[VirtualKeyMap(VirtualKey.None)]
		None = 0
	}
}
