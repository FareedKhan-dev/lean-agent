from _hidden_kit import check, find, load, report

is_ipv4 = find(load("netcheck.validate"), "is_ipv4")
allowlist = load("netcheck.allowlist")
VALID = ["192.168.0.1", "0.0.0.0", "255.255.255.255", "8.8.8.8", "10.0.0.255"]
INVALID = ["256.1.1.1", "1.2.3", "1.2.3.4.5", "1..2.3", "", "a.b.c.d", "1.2.3.-4", "+1.2.3.4",
           "1_0.2.3.4", "01.2.3.4", "1.2.3.4\n", " 1.2.3.4", "1.2.3.4 ", "127.1", "0x7f.0.0.1",
           "1.2.3.4/24", "1.2.3.4:80", "١.٢.٣.٤", "999.999.999.999",
           "::1", "2001:db8::1", "::ffff:1.2.3.4"]


def all_judged(texts, want):
    wrong = [t for t in texts if bool(is_ipv4(t)) is not want]
    assert not wrong, f"wrong for {[ascii(t) for t in wrong[:5]]}"
    return True


correct = is_ipv4 is not None and all([
    check("real addresses are accepted", lambda: all_judged(VALID, True)),
    check("everything else is refused, near misses included", lambda: all_judged(INVALID, False)),
    check("the allow-list form saves only addresses",
          lambda: allowlist.add_entry("10.1.2.3") is True and allowlist.add_entry("10.1.2.3\n") is False
          and allowlist.ALLOWED == ["10.1.2.3"])])
report(correct)
