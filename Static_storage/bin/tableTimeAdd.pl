#!/usr/bin/perl -w
use strict;
@ARGV>=2 || die"usage: perl $0 <summary> <current> [ranks] > new.summary\n";
my ($summ,$current,$ranks) = @ARGV;
open IN1,$summ || die$!;
open IN2,$current || die$!;
my $head = <IN2>;<IN1>;
my @heads = split/\s+/,$head;
my @sel;
if($ranks){
	for my $p(split/,/,$ranks){
		if($p =~ m/(\S+)\.\.(\S+)/){
			my ($n,$m) = ($1,$2);
			($n<0) && ($n+=@heads);
			($m<0) && ($m+=@heads);
			push @sel,($n..$m);
		}else{
			push @sel,$p;
		}
	}
}else{
	push @sel,(1..$#heads);
}
print $head;
my (%h1,%h2,%h);
while(<IN1>){
    my @l = split;
    my $id = shift @l;
    $h1{$id} = [@l];
    $h{$id} = 1;
}
close IN1;
while(<IN2>){
    my @l = split;
    my $id = shift @l;
    $h2{$id} = [@l];
    $h{$id} = 1;
}
close IN2;
my $d = (split/\s+/,`date`)[2];
for my $id(sort keys %h){
	my @l1 = $h1{$id} ? @{$h1{$id}} : (0) x $#heads;
	my @l2 = $h2{$id} ? @{$h2{$id}} : (0) x $#heads;
	for my $i(@sel){
		if(($l1[$i] || $l2[$i]) && $l1[$i] ne "-" && $l2[$i] ne "-"){
			$l2[$i] = sprintf("%.2f",( ($d-1)*$l1[$i] + $l2[$i]) / $d);
		}
	}
	print join("\t",$id,@l2),"\n";
}
