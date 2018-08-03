#!/usr/bin/perl -w
use strict;
use FindBin qw($Bin);
use Getopt::Long;
my ($pubdis,$XJlist,$depID,$outf,$oldf);
GetOptions("pubdis:s"=>\$pubdis,"XJlist:s"=>\$XJlist,"depID:s"=>\$depID,"outf:s"=>\$outf,"oldf:s"=>\$oldf);
@ARGV>=3 || die"usage: perl $0 JC.lib.stat.xls LC.lib.stat.xls scan.pan.xls > current.summary.stat.xls\n";
#current.summary.stat.xls form:
#1-depID 2-JC.OwnSize 3-JC.Ownperc 4-JC.ShareSize 5.JC.XJRsize 6.JC.XJperc 7.JC.XJSsize 8.JC.TotalSize
#        9-LC.OwnSize 10-LC.Ownperc 11-LC.ShareSize 12.LC.XJRsize 13.LC.XJperc 14.LC.XJSsize 15.LC.TotalSize
#16-monthXJsize 17-monthXJperc
my ($JClist,$LClist,$panlist) = @ARGV;
my %pubh;
$pubdis ||= "$Bin/pub.dis";
$depID ||= "$Bin/depID.xls";
if(-s $pubdis){
	open PU,$pubdis || die$!;
	while(<PU>){
		/\S/ || next;
		s/\s+$//g;
		my ($id,$str) = split/\s*=\s*/,$_,2;
		my @deps = split/\s*\+\s*/,$str;
		my (@keys,@values);
		for (@deps){
			my ($v,$k) = split/\*/;
			$k || (($k,$v) = ($v,1));
			push @keys,$k;
			push @values,$v;
		}
		$pubh{$id} = [[@keys],[@values]];
	}
	close PU;
}
my %stat;
my @Total;
open IN,$panlist || die$!;
<IN>;
while(<IN>){
    /^#/ && next;
    my @l = split;
	($l[3] eq "-") && next;
	$l[2] = chT($l[2]);
	my $n = ($l[1] == 1) ? 0 : 7;
	if($pubh{$l[0]}){
		my ($k,$v) = @{$pubh{$l[0]}};
		for my $i(0..$#$k){
			$stat{$k->[$i]}->[$n] += $v->[$i]*$l[2];
		}
	}else{
    	$stat{$l[0]}->[$n] += $l[2];
	}
    ($l[0] ne "Unknow" && $l[0] ne "XJ" && $l[0] ne "DATA") && ($Total[$l[1]-1] += $l[2]);
}
close IN;

my @XJR;
$XJR[0] = statL($JClist,\%pubh,3);
$XJR[1] = statL($LClist,\%pubh,10);

my @hs = qw(depID JC.OwnSize JC.Own% JC.ShareSize JC.XJRsize JC.XJ% JC.XJSsize JC.TotalSize
             LC.OwnSize LC.Own% LC.ShareSize LC.XJRsize LC.XJ% LC.XJSsize LC.TotalSize);
if($XJlist && -s $XJlist){
	push @hs,qw(MonthXJsize MonthXJ%);
	getXJstat($XJlist,$depID,\%stat,14);
}
if($outf){
	open OUT,">$outf" || die$!;
	select OUT;
}
print "#",join("\t",@hs),"\n";
for my $d(sort keys %stat){
	my @out = @{$stat{$d}};
	for (0,3,7,10){$out[$_] ||= 0;}
	if($d ne "Unknow" && $d ne "XJ" && $d ne "DATA"){
		@out[1,2] = percS($Total[0],$stat{Unknow}->[0],$out[0]);
		@out[8,9] = percS($Total[1],$stat{Unknow}->[7],$out[7]);
		@out[4,5] = percS($XJR[0],$stat{XJ}->[0],$out[3]);
		@out[11,12] = percS($XJR[1],$stat{XJ}->[7],$out[10]);
		$out[6] = $out[0] + $out[2] + $out[5];
		$out[13] = $out[7] + $out[9] + $out[12];
	}else{
		if($d eq "DATA"){
			@out[1,2,4,5,8,9,11,12] = (0) x 8;
			@out[6,13] = @out[0,7];
		}else{
			@out[1,2,4..6,8,9,11..13] = ("-") x 10;
		}
	}
	if($XJlist && -s $XJlist){
		$out[14] ||= 0;
		$out[15] ||= 0;
	}
	print join("\t",$d,@out),"\n";
}
if($outf){
	close(OUT);
	select STDOUT;
	if($oldf){
        if(-s $oldf){
            my $add = ($XJlist && -s $XJlist) ? "1..-3" : " ";
		    system"perl $Bin/tableTimeAdd.pl $oldf $outf $add > .temp.accu.table.xls
		    cp -f .temp.accu.table.xls $oldf";
        }else{
            system"cp $outf $oldf";
        }
	}
}

#======================================================================
sub getXJstat{
	my ($XJlist,$depID,$stat,$k) = @_;
	my %deph = split/\s+/,`less $depID`;
	open XJ,$XJlist || die$!;
	my $T = 0;
	chomp(my $md = `date -d "1 month ago" +"\%Y-\%m-\%d"`);
	while(<XJ>){
		my ($id,$day,$size) = (split)[-3,-2,-1];
		($day lt $md) && next;
		if($deph{$id}){
			$id = $deph{$id};
			($id =~ m/^DepID|^None|^Nohost|^Total|^\d/i) && next;
			$id =~ s/\(\d+\)//;
			$id =~ s/\_\S+//;
			$id = uc($id);
            $stat->{$id}->[$k] += $size;
			$T += $size;
		}
	}
	close XJ;
	for my $id(keys %{$stat}){
		$stat->{$id}->[$k] || next;
		$stat->{$id}->[$k+1] = sprintf("%.2f",100*$stat->{$id}->[$k]/$T);
		$stat->{$id}->[$k] = sprintf("%.2f",$stat->{$id}->[$k]/1e12);
	}
}

sub statL{
	my ($list,$pubh,$m) = @_;
	open IN2,$list || die$!;
	my $n = (`head -1 $list` =~ /^DepID/) ? 3 : 1;
	my $sum = 0;
	while(<IN2>){
		m/^DepID|^None|^Nohost|^Total|^\d/i && next;
		my @l = split;
		$l[0] =~ s/\(\d+\)//;
		$l[0] =~ s/\_\S+//;
		$l[0] = uc($l[0]);
		if($pubh->{$l[0]}){
			my ($k,$v) = @{$pubh->{$l[0]}};
			for my $i(0..$#$k){
				$stat{$k->[$i]}->[$m] += $v->[$i]*$l[$n];
			}
		}else{
    		$stat{$l[0]}->[$m] += $l[$n];
		}
		$sum += $l[$n];
	}
	close IN2;
	$sum;
}

sub percS{
	my ($T,$S,$v) = @_;
	if($T && $v){
		my $perc = $v / $T;
		my $size = $S ? sprintf("%.2f",$S*$perc) : 0;
		(sprintf("%.2f",100*$perc),$size);
	}else{
		(0,0);
	}
}
		
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
