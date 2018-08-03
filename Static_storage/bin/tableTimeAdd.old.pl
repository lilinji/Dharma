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
my $d = (split/\s+/,`date`)[2];
while(my $line1 = <IN1>){
	my $line2 = <IN2>;
	my @l1 = split/\s+/,$line1;
	my @l2 = split/\s+/,$line2;
	for my $i(@sel){
		if(($l1[$i] || $l2[$i]) && $l1[$i] ne "-" && $l2[$i] ne "-"){
			$l2[$i] = sprintf("%.2f",( ($d-1)*$l1[$i] + $l2[$i]) / $d);
		}
	}
	print join("\t",@l2),"\n";
}
close IN1;
close IN2;
