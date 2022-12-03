; ModuleID = "test_006.bc"
target triple = "x86_64-unknown-linux-gnu"
target datalayout = "e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128"

declare i32 @"leiaInteiro"()

declare float @"leiaFlutuante"()

declare void @"escrevaInteiro"(i32 %".1")

declare void @"escrevaFlutuante"(float %".1")

define i32 @"soma"(i32 %"b", i32 %"a")
{
entry:
  %"b.1" = alloca i32, align 4
  %"a.1" = alloca i32, align 4
  %"a.2" = alloca i32
  %"b.2" = alloca i32
  %".4" = load i32, i32* %"a.2"
  %".5" = load i32, i32* %"b.2"
  %"add" = add i32 %".4", %".5"
  br label %"exit"
exit:
  %"func_soma_return" = add i32 %"b", %"a"
  ret i32 %"func_soma_return"
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
  store i32 %".4", i32* %"a.1"
  %".6" = call i32 @"leiaInteiro"()
  store i32 %".6", i32* %"a"
  %".8" = call i32 @"leiaInteiro"()
  store i32 %".8", i32* %"b.1"
  %".10" = call i32 @"leiaInteiro"()
  store i32 %".10", i32* %"b"
  %"1" = alloca i32
  %".12" = load i32, i32* %"1"
  %".13" = load i32, i32* %"i"
  %"increment" = add i32 %".13", %".12"
  %".14" = load i32, i32* %"i"
  call void @"escrevaInteiro"(i32 %".14")
  %"var_for_compare" = load i32, i32* %"i", align 4
  %"check_repeat" = icmp eq i32 %"var_for_compare", 5
  br i1 %"check_repeat", label %"repeat_start", label %"repeat_end"
repeat_end:
  br label %"exit"
exit:
  ret i32 0
}
