; ModuleID = "test_007.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

define i32 @"soma"(i32 %"y", i32 %"x")
{
entry:
  %"y.1" = alloca i32, align 4
  %"x.1" = alloca i32, align 4
  %"x.2" = alloca i32
  %"y.2" = alloca i32
  %".4" = load i32, i32* %"x.2"
  %".5" = load i32, i32* %"y.2"
  %"add" = add i32 %".4", %".5"
  br label %"exit"
exit:
  %"func_soma_return" = add i32 %"y", %"x"
  ret i32 %"func_soma_return"
}

define i32 @"sub"(i32 %"t", i32 %"z")
{
entry:
  %"t.1" = alloca i32, align 4
  %"z.1" = alloca i32, align 4
  %"z.2" = alloca i32
  %"t.2" = alloca i32
  %".4" = load i32, i32* %"z.2"
  %".5" = load i32, i32* %"t.2"
  %"add" = sub i32 %".4", %".5"
  br label %"exit"
exit:
  %"func_sub_return" = add i32 %"t", %"z"
  ret i32 %"func_sub_return"
}

define i32 @"main"()
{
entry:
  %"a" = alloca i32, align 4
  %"b" = alloca i32, align 4
  %"c" = alloca i32, align 4
  %"i" = alloca i32, align 4
  store i32 0, i32* %"i"
  br label %"repeat_start"
repeat_start:
  %".4" = call i32 @"leiaInteiro"()
  store i32 %".4", i32* %"a"
  %".6" = call i32 @"leiaInteiro"()
  store i32 %".6", i32* %"b"
  %"1" = alloca i32
  %".8" = load i32, i32* %"1"
  %".9" = load i32, i32* %"i"
  %"increment" = add i32 %".9", %".8"
  %".10" = load i32, i32* %"i"
  call void @"escrevaInteiro"(i32 %".10")
  %"var_for_compare" = load i32, i32* %"i", align 4
  %"check_repeat" = icmp eq i32 %"var_for_compare", 5
  br i1 %"check_repeat", label %"repeat_start", label %"repeat_end"
repeat_end:
  br label %"exit"
exit:
  ret i32 0
}
