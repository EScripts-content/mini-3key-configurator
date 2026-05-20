using System;

namespace RSoft.MacroPad.BLL.Infrasturture.Model
{
	// Token: 0x02000036 RID: 54
	[Flags]
	public enum VirtualKey
	{
		// Token: 0x04000116 RID: 278
		KeyCode = 65535,
		// Token: 0x04000117 RID: 279
		Modifiers = -65536,
		// Token: 0x04000118 RID: 280
		None = 0,
		// Token: 0x04000119 RID: 281
		LButton = 1,
		// Token: 0x0400011A RID: 282
		RButton = 2,
		// Token: 0x0400011B RID: 283
		Cancel = 3,
		// Token: 0x0400011C RID: 284
		MButton = 4,
		// Token: 0x0400011D RID: 285
		XButton1 = 5,
		// Token: 0x0400011E RID: 286
		XButton2 = 6,
		// Token: 0x0400011F RID: 287
		Back = 8,
		// Token: 0x04000120 RID: 288
		Tab = 9,
		// Token: 0x04000121 RID: 289
		LineFeed = 10,
		// Token: 0x04000122 RID: 290
		Clear = 12,
		// Token: 0x04000123 RID: 291
		Return = 13,
		// Token: 0x04000124 RID: 292
		Enter = 13,
		// Token: 0x04000125 RID: 293
		ShiftKey = 16,
		// Token: 0x04000126 RID: 294
		ControlKey = 17,
		// Token: 0x04000127 RID: 295
		Menu = 18,
		// Token: 0x04000128 RID: 296
		Pause = 19,
		// Token: 0x04000129 RID: 297
		Capital = 20,
		// Token: 0x0400012A RID: 298
		CapsLock = 20,
		// Token: 0x0400012B RID: 299
		KanaMode = 21,
		// Token: 0x0400012C RID: 300
		HanguelMode = 21,
		// Token: 0x0400012D RID: 301
		HangulMode = 21,
		// Token: 0x0400012E RID: 302
		JunjaMode = 23,
		// Token: 0x0400012F RID: 303
		FinalMode = 24,
		// Token: 0x04000130 RID: 304
		HanjaMode = 25,
		// Token: 0x04000131 RID: 305
		KanjiMode = 25,
		// Token: 0x04000132 RID: 306
		Escape = 27,
		// Token: 0x04000133 RID: 307
		IMEConvert = 28,
		// Token: 0x04000134 RID: 308
		IMENonconvert = 29,
		// Token: 0x04000135 RID: 309
		IMEAccept = 30,
		// Token: 0x04000136 RID: 310
		IMEAceept = 30,
		// Token: 0x04000137 RID: 311
		IMEModeChange = 31,
		// Token: 0x04000138 RID: 312
		Space = 32,
		// Token: 0x04000139 RID: 313
		Prior = 33,
		// Token: 0x0400013A RID: 314
		PageUp = 33,
		// Token: 0x0400013B RID: 315
		Next = 34,
		// Token: 0x0400013C RID: 316
		PageDown = 34,
		// Token: 0x0400013D RID: 317
		End = 35,
		// Token: 0x0400013E RID: 318
		Home = 36,
		// Token: 0x0400013F RID: 319
		Left = 37,
		// Token: 0x04000140 RID: 320
		Up = 38,
		// Token: 0x04000141 RID: 321
		Right = 39,
		// Token: 0x04000142 RID: 322
		Down = 40,
		// Token: 0x04000143 RID: 323
		Select = 41,
		// Token: 0x04000144 RID: 324
		Print = 42,
		// Token: 0x04000145 RID: 325
		Execute = 43,
		// Token: 0x04000146 RID: 326
		Snapshot = 44,
		// Token: 0x04000147 RID: 327
		PrintScreen = 44,
		// Token: 0x04000148 RID: 328
		Insert = 45,
		// Token: 0x04000149 RID: 329
		Delete = 46,
		// Token: 0x0400014A RID: 330
		Help = 47,
		// Token: 0x0400014B RID: 331
		D0 = 48,
		// Token: 0x0400014C RID: 332
		D1 = 49,
		// Token: 0x0400014D RID: 333
		D2 = 50,
		// Token: 0x0400014E RID: 334
		D3 = 51,
		// Token: 0x0400014F RID: 335
		D4 = 52,
		// Token: 0x04000150 RID: 336
		D5 = 53,
		// Token: 0x04000151 RID: 337
		D6 = 54,
		// Token: 0x04000152 RID: 338
		D7 = 55,
		// Token: 0x04000153 RID: 339
		D8 = 56,
		// Token: 0x04000154 RID: 340
		D9 = 57,
		// Token: 0x04000155 RID: 341
		A = 65,
		// Token: 0x04000156 RID: 342
		B = 66,
		// Token: 0x04000157 RID: 343
		C = 67,
		// Token: 0x04000158 RID: 344
		D = 68,
		// Token: 0x04000159 RID: 345
		E = 69,
		// Token: 0x0400015A RID: 346
		F = 70,
		// Token: 0x0400015B RID: 347
		G = 71,
		// Token: 0x0400015C RID: 348
		H = 72,
		// Token: 0x0400015D RID: 349
		I = 73,
		// Token: 0x0400015E RID: 350
		J = 74,
		// Token: 0x0400015F RID: 351
		K = 75,
		// Token: 0x04000160 RID: 352
		L = 76,
		// Token: 0x04000161 RID: 353
		M = 77,
		// Token: 0x04000162 RID: 354
		N = 78,
		// Token: 0x04000163 RID: 355
		O = 79,
		// Token: 0x04000164 RID: 356
		P = 80,
		// Token: 0x04000165 RID: 357
		Q = 81,
		// Token: 0x04000166 RID: 358
		R = 82,
		// Token: 0x04000167 RID: 359
		S = 83,
		// Token: 0x04000168 RID: 360
		T = 84,
		// Token: 0x04000169 RID: 361
		U = 85,
		// Token: 0x0400016A RID: 362
		V = 86,
		// Token: 0x0400016B RID: 363
		W = 87,
		// Token: 0x0400016C RID: 364
		X = 88,
		// Token: 0x0400016D RID: 365
		Y = 89,
		// Token: 0x0400016E RID: 366
		Z = 90,
		// Token: 0x0400016F RID: 367
		LWin = 91,
		// Token: 0x04000170 RID: 368
		RWin = 92,
		// Token: 0x04000171 RID: 369
		Apps = 93,
		// Token: 0x04000172 RID: 370
		Sleep = 95,
		// Token: 0x04000173 RID: 371
		NumPad0 = 96,
		// Token: 0x04000174 RID: 372
		NumPad1 = 97,
		// Token: 0x04000175 RID: 373
		NumPad2 = 98,
		// Token: 0x04000176 RID: 374
		NumPad3 = 99,
		// Token: 0x04000177 RID: 375
		NumPad4 = 100,
		// Token: 0x04000178 RID: 376
		NumPad5 = 101,
		// Token: 0x04000179 RID: 377
		NumPad6 = 102,
		// Token: 0x0400017A RID: 378
		NumPad7 = 103,
		// Token: 0x0400017B RID: 379
		NumPad8 = 104,
		// Token: 0x0400017C RID: 380
		NumPad9 = 105,
		// Token: 0x0400017D RID: 381
		Multiply = 106,
		// Token: 0x0400017E RID: 382
		Add = 107,
		// Token: 0x0400017F RID: 383
		Separator = 108,
		// Token: 0x04000180 RID: 384
		Subtract = 109,
		// Token: 0x04000181 RID: 385
		Decimal = 110,
		// Token: 0x04000182 RID: 386
		Divide = 111,
		// Token: 0x04000183 RID: 387
		F1 = 112,
		// Token: 0x04000184 RID: 388
		F2 = 113,
		// Token: 0x04000185 RID: 389
		F3 = 114,
		// Token: 0x04000186 RID: 390
		F4 = 115,
		// Token: 0x04000187 RID: 391
		F5 = 116,
		// Token: 0x04000188 RID: 392
		F6 = 117,
		// Token: 0x04000189 RID: 393
		F7 = 118,
		// Token: 0x0400018A RID: 394
		F8 = 119,
		// Token: 0x0400018B RID: 395
		F9 = 120,
		// Token: 0x0400018C RID: 396
		F10 = 121,
		// Token: 0x0400018D RID: 397
		F11 = 122,
		// Token: 0x0400018E RID: 398
		F12 = 123,
		// Token: 0x0400018F RID: 399
		F13 = 124,
		// Token: 0x04000190 RID: 400
		F14 = 125,
		// Token: 0x04000191 RID: 401
		F15 = 126,
		// Token: 0x04000192 RID: 402
		F16 = 127,
		// Token: 0x04000193 RID: 403
		F17 = 128,
		// Token: 0x04000194 RID: 404
		F18 = 129,
		// Token: 0x04000195 RID: 405
		F19 = 130,
		// Token: 0x04000196 RID: 406
		F20 = 131,
		// Token: 0x04000197 RID: 407
		F21 = 132,
		// Token: 0x04000198 RID: 408
		F22 = 133,
		// Token: 0x04000199 RID: 409
		F23 = 134,
		// Token: 0x0400019A RID: 410
		F24 = 135,
		// Token: 0x0400019B RID: 411
		NumLock = 144,
		// Token: 0x0400019C RID: 412
		Scroll = 145,
		// Token: 0x0400019D RID: 413
		LShiftKey = 160,
		// Token: 0x0400019E RID: 414
		RShiftKey = 161,
		// Token: 0x0400019F RID: 415
		LControlKey = 162,
		// Token: 0x040001A0 RID: 416
		RControlKey = 163,
		// Token: 0x040001A1 RID: 417
		LMenu = 164,
		// Token: 0x040001A2 RID: 418
		RMenu = 165,
		// Token: 0x040001A3 RID: 419
		BrowserBack = 166,
		// Token: 0x040001A4 RID: 420
		BrowserForward = 167,
		// Token: 0x040001A5 RID: 421
		BrowserRefresh = 168,
		// Token: 0x040001A6 RID: 422
		BrowserStop = 169,
		// Token: 0x040001A7 RID: 423
		BrowserSearch = 170,
		// Token: 0x040001A8 RID: 424
		BrowserFavorites = 171,
		// Token: 0x040001A9 RID: 425
		BrowserHome = 172,
		// Token: 0x040001AA RID: 426
		VolumeMute = 173,
		// Token: 0x040001AB RID: 427
		VolumeDown = 174,
		// Token: 0x040001AC RID: 428
		VolumeUp = 175,
		// Token: 0x040001AD RID: 429
		MediaNextTrack = 176,
		// Token: 0x040001AE RID: 430
		MediaPreviousTrack = 177,
		// Token: 0x040001AF RID: 431
		MediaStop = 178,
		// Token: 0x040001B0 RID: 432
		MediaPlayPause = 179,
		// Token: 0x040001B1 RID: 433
		LaunchMail = 180,
		// Token: 0x040001B2 RID: 434
		SelectMedia = 181,
		// Token: 0x040001B3 RID: 435
		LaunchApplication1 = 182,
		// Token: 0x040001B4 RID: 436
		LaunchApplication2 = 183,
		// Token: 0x040001B5 RID: 437
		OemSemicolon = 186,
		// Token: 0x040001B6 RID: 438
		Oem1 = 186,
		// Token: 0x040001B7 RID: 439
		Oemplus = 187,
		// Token: 0x040001B8 RID: 440
		Oemcomma = 188,
		// Token: 0x040001B9 RID: 441
		OemMinus = 189,
		// Token: 0x040001BA RID: 442
		OemPeriod = 190,
		// Token: 0x040001BB RID: 443
		OemQuestion = 191,
		// Token: 0x040001BC RID: 444
		Oem2 = 191,
		// Token: 0x040001BD RID: 445
		Oemtilde = 192,
		// Token: 0x040001BE RID: 446
		Oem3 = 192,
		// Token: 0x040001BF RID: 447
		OemOpenBrackets = 219,
		// Token: 0x040001C0 RID: 448
		Oem4 = 219,
		// Token: 0x040001C1 RID: 449
		OemPipe = 220,
		// Token: 0x040001C2 RID: 450
		Oem5 = 220,
		// Token: 0x040001C3 RID: 451
		OemCloseBrackets = 221,
		// Token: 0x040001C4 RID: 452
		Oem6 = 221,
		// Token: 0x040001C5 RID: 453
		OemQuotes = 222,
		// Token: 0x040001C6 RID: 454
		Oem7 = 222,
		// Token: 0x040001C7 RID: 455
		Oem8 = 223,
		// Token: 0x040001C8 RID: 456
		OemBackslash = 226,
		// Token: 0x040001C9 RID: 457
		Oem102 = 226,
		// Token: 0x040001CA RID: 458
		ProcessKey = 229,
		// Token: 0x040001CB RID: 459
		Packet = 231,
		// Token: 0x040001CC RID: 460
		Attn = 246,
		// Token: 0x040001CD RID: 461
		Crsel = 247,
		// Token: 0x040001CE RID: 462
		Exsel = 248,
		// Token: 0x040001CF RID: 463
		EraseEof = 249,
		// Token: 0x040001D0 RID: 464
		Play = 250,
		// Token: 0x040001D1 RID: 465
		Zoom = 251,
		// Token: 0x040001D2 RID: 466
		NoName = 252,
		// Token: 0x040001D3 RID: 467
		Pa1 = 253,
		// Token: 0x040001D4 RID: 468
		OemClear = 254,
		// Token: 0x040001D5 RID: 469
		Shift = 65536,
		// Token: 0x040001D6 RID: 470
		Control = 131072,
		// Token: 0x040001D7 RID: 471
		Alt = 262144
	}
}
