#!/usr/bin/perl -w
use strict;
use FindBin qw($Bin);
@ARGV || die"usage: perl $0 <pan.list> [dep.group.xls] > out.scan.xls\n";
my ($panl,$group) = @ARGV;
$group ||= "$Bin/dep.group.xls";
my %grouph = split/\s+/,`less $group`;
print "#",join("\t",qw(Group DiskLevel Size Used Avail Use% Pathway)),"\n";
open IN,$panl || die$!;
while(<IN>){
    my ($d,$t) = split;
    my @size = (split/\s+/,`df -h $d`)[-5..-1];
    my $od = 0;
    my $as = 0;
    my $os = chT($size[0]);
    for (`ls $d`){
        chomp;
        (-d "$d/$_") || next;
        my @o = (split/\s+/,`df -h $d/$_`)[-5..-1];
        ($size[0] eq $o[0]) && next;
        $o[-1] .= "/$_";
        s/\d+$//;
        my $sign = uc($_);
        if($grouph{$o[-1]}){
            $sign = $grouph{$o[-1]};
        }elsif($grouph{$sign}){
            $sign = $grouph{$sign};
        }else{
            $sign = "Unknow";
        }
        print join("\t",$sign,$t,@o),"\n";
        $od++;
        $as += chT($o[0]);
    }
    if($od == 0){
        print join("\t",$grouph{$d} || "Unknow",$t,@size),"\n";
    }elsif($os > $as){
        print join("\t","Unknow",$t,($os-$as)."T",qw(- - -),$d),"\n";
    }
}
close IN;
sub chT{
    my $s = shift;
    if($s =~ s/P$//){
        $s *= 1000;
    }elsif($s =~ s/G$//){
        $s /= 1000;
    }elsif($s =~ s/K$//){
        $s /= 1000000;
    }else{
        $s =~ s/T//;
    }
    $s;
}
